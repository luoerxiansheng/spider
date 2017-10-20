# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from jibingbaike.items import JibingbaikeItem


class A39jibingSpider(scrapy.Spider):
    name = "a39jibing"
    # allowed_domains = [""]
    start_urls = (
        'http://jbk.39.net/bw/',
    )

    def parse(self, response):

        print len(response.xpath("//div[@id='cond_box1']/dl|//div[@id='cond_box1']/div"))
        #大部位
        for x in response.xpath("//div[@id='cond_box1']/dl|//div[@id='cond_box1']/div"):
            #判断是否有dd标签
            if len(x.xpath("./dd")) > 0:
                #每次的大部位
                part = x.xpath("./dt/a/text()").extract()[0]

                #循环dd标签的小部位
                for j in x.xpath("./dd/a"):
                    #小部位
                    apparatus =  j.xpath("./text()").extract()[0]

                    yield scrapy.Request(url='http://jbk.39.net'+j.xpath("./@href").extract()[0],callback=self.parlist,meta={'part':part,'apparatus':apparatus})
            else:
                #div 的格式和dl不一样
                part = x.xpath("./a/text()").extract()[0]

                yield scrapy.Request(url='http://jbk.39.net'+x.xpath("./a/@href").extract()[0],callback=self.parlist,meta={'part':part,'apparatus':''})

    def parlist(self,response):

        part = response.meta['part']

        apparatus = response.meta['apparatus']

        #疾病列表
        for x in response.xpath("//div[@class='res_list']//h3"):

            url = url = x.xpath("./a/@href").extract()[0]+'jbzs/'
            #进详情页
            yield scrapy.Request(url = x.xpath("./a/@href").extract()[0]+'jbzs/',callback=self.parmore,meta={'part':part,'apparatus':apparatus,'url':url})
        #翻页规则
        if len(response.xpath("//a[@class='sp-a']")) > 0:

            if len(response.xpath("//a[@class='sp-a']")) == 4:

                yield scrapy.Request(url = 'http://jbk.39.net'+response.xpath("//a[@class='sp-a'][3]/@href").extract()[0],callback=self.parlist,meta={'part':part,'apparatus':apparatus})

            elif len(response.xpath("//a[@class='sp-a']")) == 2 and response.xpath("//a[@class='sp-a'][1]/text()").extract()[0] == u'下页':

                yield scrapy.Request(url='http://jbk.39.net' + response.xpath("//a[@class='sp-a'][1]/@href").extract()[0],callback=self.parlist, meta={'part': part, 'apparatus': apparatus})

    def parmore(self,response):

        item = JibingbaikeItem()
        #来源
        item['source'] = '疾病百科'

        item['body'] = response.body
        #url
        item['URL'] = response.meta['url']
        #大部位
        item['part'] = response.meta['part']
        #小部位
        item['apparatus'] = response.meta['apparatus']
        #病称
        item['illness'] = response.xpath("//h1/text()").extract()[0]
        #简介
        item['origin'] = response.xpath("//dl[@class='intro']/dd/text()").extract()[0].strip()
        #科室
        item['division'] = ','.join(response.xpath("//div[@class='chi-know']/dl[3]/dd[1]/a/text()").extract()[0].split())
        #药品
        medicine = ''

        for x in response.xpath("//a[@class='a1']/text()"):

            medicine += x.extract()+','
        #逗号切片
        if medicine.find('...'):
            #去除...
            medicine = ''.join(medicine.split('...'))

        item['medicine'] = medicine[:-1]
        #并发症网址
        if len(response.xpath("//div[@class='chi-know']/dl[2]/dd[last()]/a[last()]/@href")) > 0:

            b_url = response.xpath("//div[@class='chi-know']/dl[2]/dd[last()]/a[last()]/@href").extract()[0]

        else:
            #没有的话 给空
            b_url = ''

            item['complication'] = ''
        try:
            #出错的话执行并发症
            yield scrapy.Request(url = response.xpath("//div[@class='chi-know']/dl[2]/dd[last()-1]/a[last()]/@href").extract()[0],callback=self.parsymptom,meta={'item':item,'b_url':b_url})

        except:
            #如果取不到适应症
            item['symptom'] = ''

            if len(b_url) > 0:

                yield scrapy.Request(url=b_url, callback=self.parcomplication, meta={'item': item})


    #适应症界面
    def parsymptom(self,response):

        item = response.meta['item']
        #症状
        symptom = ''

        for x in response.xpath("//dl[@class='links']/dd[last()]/a/text()"):

            symptom += x.extract()+','

        item['symptom'] = symptom[:-1]

        if len(response.meta['b_url']) > 0:

            yield scrapy.Request(url = response.meta['b_url'],callback=self.parcomplication,meta={'item':item})

    #并发症页面
    def parcomplication(self,response):

        item = response.meta['item']

        complication = ''

        for x in response.xpath("//dl[@class='links']/dd[last()]/a/text()"):

            complication += x.extract() +','

        item['complication'] = complication[:-1]

        return item













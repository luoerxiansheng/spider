# -*- coding: utf-8 -*-
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time

from xunyiwenyao.items import XunyiwenyaoItem

class XunyiSpider(scrapy.Spider):
    name = "xunyi"
    # allowed_domains = [""]
    # start_urls = (
    #     'http://jib.xywy.com/html/toubu.html',
    # )
    def start_requests(self):

        urlist = ['http://jib.xywy.com/html/toubu.html',
                  'http://jib.xywy.com/html/jingbu.html',
                  'http://jib.xywy.com/html/sizhi.html',
                  'http://jib.xywy.com/html/xiongbu.html',
                  'http://jib.xywy.com/html/fubu.html',
                  'http://jib.xywy.com/html/yaobu.html',
                  'http://jib.xywy.com/html/shengzhibuwei.html',
                  'http://jib.xywy.com/html/pifu.html',
                  'http://jib.xywy.com/html/quanshen.html',
                  'http://jib.xywy.com/html/paixiebuwei.html']

        for x in range(len(urlist)):

            yield scrapy.Request(url = urlist[x],callback=self.parse,meta={'x':x})


    def parse(self, response):

        x = response.meta['x']+1
        #大部位名称
        d_name = response.xpath("//li[@class='pr'][%s]/a/text()"%x).extract()[0]
        print d_name
        #小部位名称
        x_name = response.xpath("//strong[@class='fb f14']/text()").extract()[0]
        print x_name
        #判断结构是否标准 以头部为例
        if len(response.xpath("//div[@class='ks-ill-box pb20']")) > 0:
            #循环一级模块
            for x in response.xpath("//div[@class='ks-ill-box pb20']"):
                #判断模块中是否有更多标签
                if len(x.xpath("./div/a")) > 0:
                    #跟进更多标签页面
                    yield scrapy.Request(url = 'http://jib.xywy.com'+x.xpath("./div/a/@href").extract()[0],callback=self.parse_more,meta={'d_name':d_name})

                else:
                    for x in response.xpath("./li"):

                        b_name = x.xpath("./a/text()").extract()[0]

                        #跟进无更多标签的页面

                        url ='http://jib.xywy.com'+x.xpath('./a/@href').extract()[0]

                        yield scrapy.Request(url ='http://jib.xywy.com'+x.xpath('./a/@href').extract()[0],callback=self.parse_details,meta={'d_name':d_name,'x_name':x_name,'b_name':b_name,'url':url})

        else:
            #非标准页面 循环
            for x in response.xpath("//div[@class='ks-ill-txt mt20']//li"):

                b_name = x.xpath("./a/text()").extract()[0]

                # 跟进无更多标签的页面
                url = 'http://jib.xywy.com' + x.xpath('./a/@href').extract()[0]

                yield scrapy.Request(url='http://jib.xywy.com' + x.xpath('./a/@href').extract()[0], callback=self.parse_details,meta={'d_name': d_name, 'x_name': x_name,'b_name':b_name,'url':url})

    def parse_more(self,response):
        #更多标签的界面数据
        urllist = response.xpath("//div[@class='ks-ill-txt mt20']//li")
        #取出数据 继续传递 大部位名 小部位名
        d_name = response.meta['d_name']
        x_name = response.xpath("//strong[@class='fb f14']/text()").extract()[0]

        for x in urllist:

            b_name = x.xpath("./a/text()").extract()[0]
            #进详情页面
            url = 'http://jib.xywy.com' + x.xpath("./a/@href").extract()[0]

            yield scrapy.Request(url = 'http://jib.xywy.com' + x.xpath("./a/@href").extract()[0],callback=self.parse_details,meta={'d_name':d_name,'b_name':b_name,'x_name':x_name,'url':url})

    #详细介绍的页面数据
    def parse_details(self,response):

        item = XunyiwenyaoItem()

        body = response.body

        item['body'] =body

        item['wangzhan_name'] = '寻医问药'

        item['URL'] = response.meta['url']

        item['d_name'] = response.meta['d_name']
        #去掉常见病
        item['x_name'] = response.meta['x_name'][:response.meta['x_name'].find(u'常见病')]

        # b_name = response.meta['b_name']
        # #病称规范化
        # if b_name.find('...') > 0:
        #
        #     b_name = b_name[:-3]

        item['b_name'] = response.xpath("//div[@class='jb-name fYaHei gre']/text()").extract()[0]

        drug = ''
        #药品循环
        for x in response.xpath("//p[5]//span[@class='fl treat-right']/a/text()"):
            drug += x.extract()+','

        item['y_name'] = drug[:-1]

        # item['zhiyu_name'] = response.xpath("//p[4]/span[@class='fl treat-right']/text()").extract()[0]

        item["ke_name"] = ','.join(response.xpath("//p[1]/span[@class='fl treat-right']/text()").extract()[0].split())


        z_url = 'http://jib.xywy.com' + response.xpath("//div[@class='fl jib-common-sense']/p[6]/span[3]/a/@href").extract()[0]

        #症状表现的页面
        yield scrapy.Request(url = 'http://jib.xywy.com'+response.xpath("//div[@class='fl jib-common-sense']/p[5]/span[3]/a/@href").extract()[0],callback=self.parse_symptom,meta={'z_url':z_url,'item':item})

    #症状详情页面
    def parse_symptom(self,response):

        item = response.meta['item']

        symptom = ''

        for x in response.xpath("//div[@class='jib-articl fr f14 jib-lh-articl']/span/a/text()"):

            symptom+=x.extract()+','
        #查找是否有...
        if symptom.find('...') > 0:

            symptom = ''.join(symptom.split('...'))

        item['z_name'] = symptom[:-1]


        yield scrapy.Request(url =response.meta['z_url'],callback=self.parse_complication,meta={'item':item} )

    #并发症详情页面
    def parse_complication(self,response):

        item = response.meta['item']

        complication = ''

        for x in response.xpath("//div[@class='jib-articl fr f14 jib-lh-articl']//span/a/text()"):

            complication+=x.extract()+','

        item['bingfa_name'] = complication[:-1]

        yield scrapy.Request(url='http://jib.xywy.com'+response.xpath("//ul[@class='dep-nav f14 clearfix']/li[2]/a/@href").extract()[0],callback=self.pargaishu,meta={'item':item})
    #简介页面
    def pargaishu(self,response):

        item = response.meta['item']

        item['jianjie'] = response.xpath("//div[@class='jib-articl-con jib-lh-articl']/p/text()").extract()[0].strip()

        return item
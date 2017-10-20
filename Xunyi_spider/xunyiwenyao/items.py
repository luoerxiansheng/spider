# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XunyiwenyaoItem(scrapy.Item):

    #网站名称
    wangzhan_name = scrapy.Field()
    #大部位
    d_name = scrapy.Field()
    # 小部位
    x_name = scrapy.Field()
    # 病称
    b_name = scrapy.Field()
    # 症状
    z_name = scrapy.Field()
    #局部临床症状
    jubu_name = scrapy.Field()
    #全身临床症状
    quan_name = scrapy.Field()
    # 药品
    y_name = scrapy.Field()
    # #治愈
    # zhiyu_name = scrapy.Field()
    #科室
    ke_name = scrapy.Field()
    #并发症
    bingfa_name = scrapy.Field()
    #详细并发症
    xianxibing_name = scrapy.Field()
    #治疗费用
    feiyong_name = scrapy.Field()
    #治疗方式
    fangshi_name = scrapy.Field()
    #传染性
    chuanran_name = scrapy.Field()
    #RUL
    URL = scrapy.Field()

    jianjie  = scrapy.Field()

    body = scrapy.Field()



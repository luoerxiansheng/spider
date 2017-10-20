# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JibingbaikeItem(scrapy.Item):
    # 来源
    source = scrapy.Field()
    # 部位
    part = scrapy.Field()
    # 病称
    illness = scrapy.Field()
    # 详细症状
    diagnose = scrapy.Field()
    # 药品名
    medicine = scrapy.Field()
    # 并发症
    complication = scrapy.Field()
    # 介绍
    origin = scrapy.Field()
    # 科室
    division = scrapy.Field()
    # 症状
    symptom = scrapy.Field()
    #url
    URL = scrapy.Field()
    #起因
    cause = scrapy.Field()
    #小部位
    apparatus = scrapy.Field()

    body = scrapy.Field()

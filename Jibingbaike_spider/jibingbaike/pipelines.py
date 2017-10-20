# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import MySQLdb


class JibingbaikePipeline(object):
    def __init__(self):
        self.f = open('yao.json', 'w')

    def process_item(self, item, spider):
        itemstr = json.dumps(dict(item), ensure_ascii=False)

        self.f.write(itemstr)

        return item

    def close_spider(self, spider):
        self.f.close()

class XunyiwenyaoHTML(object):

    def __init__(self):

        self.num = 1


    def process_item(self, item, spider):

        self.f = open('html/jibingbaike%s.html'%self.num, 'w')

        self.f.write(item['body'])

        self.num += 1

        return item

    def close_spider(self,spider):

        self.f.close()



class WriteMysql():

    def __init__(self):

        self.coon = MySQLdb.connect('10.10.2.159', 'root', 'ea8bG?Ckqe', 'data_warehouse', charset='utf8',use_unicode = True)

        self.cursor = self.coon.cursor()

    def process_item(self,item,spider):

        csql = "select * from ods_disease where disease = '%s'"%item['illness']

        cur = self.cursor.execute(csql)

        if cur ==0:

            print '=' * 100
            print '数据库中无此数据，此条数据存入数据库'
            print '=' * 100
            xsql = 'insert into ods_disease(id,source,part,disease,intro,symptom,medicine,division,complication,url,small_parts) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            self.cursor.execute(xsql,(0,item['source'],item['part'],item['illness'],item["origin"],item['symptom'],item['medicine'],item['division'],item["complication"],item['URL'],item['apparatus']))

            self.coon.commit()

        return item


class UpdateMysql():

    def __init__(self):
        self.coon = MySQLdb.connect('10.10.2.159', 'root', 'ea8bG?Ckqe', 'data_warehouse', charset='utf8',
                                    use_unicode=True)

        self.cursor = self.coon.cursor()

    def process_item(self, item, spider):

        csql = "select * from ods_disease where source = '%s',part= '%s',disease= '%s',intro= '%s',symptom= '%s',medicine= '%s',division= '%s',complication= '%s',url= '%s',small_parts= '%s'" % (item['source'], item['part'], item['illness'], item["origin"], item['symptom'], item['medicine'],
            item['division'], item["complication"], item['URL'], item['apparatus'])

        cur = self.cursor.execute(csql)

        if cur == 0:

            print '=' * 100
            print '更新一条数据'
            print '=' * 100

            xsql = "update ods_disease set source = '%s',part= '%s',disease= '%s',intro= '%s',symptom= '%s',medicine= '%s',division= '%s',complication= '%s',url= '%s',small_parts= '%s' where url = '%s" %(item['source'], item['part'], item['illness'], item["origin"], item['symptom'], item['medicine'],
            item['division'], item["complication"], item['URL'], item['apparatus'],item['URL'])

            self.cursor.execute(xsql)

            self.coon.commit()

        return item
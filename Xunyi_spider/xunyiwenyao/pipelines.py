# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import json
import MySQLdb

class XunyiwenyaoJson(object):

    def __init__(self):

        self.f = open('yao.json','w')

    def process_item(self, item, spider):

        itemstr = json.dumps(dict(item),ensure_ascii=False)

        self.f.write(itemstr)

        return item

    def close_spider(self,spider):

        self.f.close()


class XunyiwenyaoPipeline(object):

    def __init__(self):

        self.num = 1
        # self.f = open('yao.txt','w')

    def process_item(self, item, spider):

        # itemstr = json.dumps(dict(item),ensure_ascii=False)
        self.f = open('/home/luoerxiansheng/Desktop/xunyiwenyao/xunyiwenyao/spiders/html/xunyiwenyao%s.html'%self.num, 'w')

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

        csql = "select * from ods_disease where url = '%s'"%item['URL']

        cur = self.cursor.execute(csql)

        if cur ==0:

            print '=' * 100
            print '数据库中无此数据，此条数据存入数据库'
            print '=' * 100
            xsql = 'insert into ods_disease(id,source,part,small_parts,disease,symptom,medicine,division,complication,intro,url) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            self.cursor.execute(xsql,(0,item['wangzhan_name'],item['d_name'],item['x_name'],item['b_name'],item['z_name'],item['y_name'],item['ke_name'],item['bingfa_name'],item['jianjie'],item['URL'],))

            self.coon.commit()

        return item

class UpdateMysql():

    def __init__(self):

        self.coon = MySQLdb.connect('10.10.2.159', 'root', 'ea8bG?Ckqe', 'data_warehouse', charset='utf8',use_unicode = True)

        self.cursor = self.coon.cursor()

    def process_item(self,item,spider):

        csql = "select * from ods_disease where source = '%s',part = '%s',small_parts = '%s',disease = '%s',symptom = '%s',medicine = '%s',division = '%s',complication = '%s',intro = '%s',url = '%s'"%(
            item['wangzhan_name'],item['d_name'],item['x_name'],item['b_name'],item['z_name'],item['y_name'],item['ke_name'],item['bingfa_name'],item['jianjie'],item['URL'])

        cur = self.cursor.execute(csql)

        if cur ==0:

            print '=' * 100
            print '更新一条数据'
            print '=' * 100
            xsql = "update ods_disease set source = '%s',part = '%s',small_parts = '%s',disease = '%s',symptom = '%s',medicine = '%s',division = '%s',complication = '%s',intro = '%s',url = '%s' where url ='%s'"%(
            item['wangzhan_name'], item['d_name'], item['x_name'], item['b_name'], item['z_name'], item['y_name'],item['ke_name'], item['bingfa_name'], item['jianjie'], item['URL'],item['URL']
            )

            self.cursor.execute(xsql)

            self.coon.commit()

        return item
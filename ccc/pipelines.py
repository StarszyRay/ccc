# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class CccPipeline(object):

    def open_spider(self, spider):
        self.csv_marki_writer = csv.writer(open('marki_{0}.csv'.format(spider.name), 'w'))
        self.csv_marki_writer.writerow({'marka', 'opis_marki', 'zdjecie_marki'})
        self.ids_seen = set()
        self.markiT = []

    def close_spider(self, spider):
        s = set()
        for element in self.markiT:
            s.add(element)
            #self.csv_marki_writer.writerow([element[0], element[1], element[2]])
        print(s)
        pass

    def process_item(self, item, spider):
        self.markiT += (item['marka'], item['opis_marki'], item['zdjecie_marki'])
        return item

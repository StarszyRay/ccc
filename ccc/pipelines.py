# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class CccPipeline(object):

    def open_spider(self, spider):
        self.csv_marki_writer = csv.writer(open('marki_{0}.csv'.format(spider.name), 'w', encoding='utf-8', newline=''), delimiter='|')
        self.csv_marki_writer.writerow(['marka', 'opis_marki', 'zdjecie_marki', 'aktywny'])
        self.ids_seen = set()
        self.markiT = []

    def close_spider(self, spider):
        s = set()
        for element in self.markiT:
            #print(element)
            #print('\n--------------------------\n')
            s.add(element)
            #self.csv_marki_writer.writerow(element)

        for se in s:
            self.csv_marki_writer.writerow(se)
            #print(se)
            #print('\n-------------------------\n')
        pass

    def process_item(self, item, spider):
        self.markiT.append((item['marka'], item['opis_marki'], item['zdjecie_marki'], item['wyswietlany']))
        return item

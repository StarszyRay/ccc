# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import random

class CccPipeline(object):

    def open_spider(self, spider):
        self.csv_marki_writer = csv.writer(open('marki_{0}.csv'.format(spider.name), 'w', encoding='utf-8', newline=''), delimiter='|')
        self.csv_marki_writer.writerow(['marka', 'opis_marki', 'zdjecie_marki', 'aktywny'])
        #Index	Attribute(Name:Type:Pos)	Value(Value:Pos)	Count
        if spider.name == 'obowie':
            self.csv_kombinacje_writer = csv.writer(open('kombinacje_{0}.csv'.format(spider.name), 'w', encoding='utf-8', newline=''),
                                               delimiter='|')
            self.csv_kombinacje_writer.writerow(['Index', 'Attribute(Name:Type:Pos)', 'Value(Value:Pos)', 'Count'])
        self.ids_seen = set()
        self.markiT = []

    def close_spider(self, spider):
        s = set()
        for element in self.markiT:
            s.add(element)
        for se in s:
            self.csv_marki_writer.writerow(se)
        pass

    def process_item(self, item, spider):
        self.markiT.append((item['marka'], item['opis_marki'], item['zdjecie_marki'], item['wyswietlany']))
        if spider.name == 'obowie':
            for rozmiar in (item['rozmiary']).split(','):
                self.csv_kombinacje_writer.writerow([ item['indeks'], "Size:select:0", "{0}:00:00".format(rozmiar), random.randint(10, 100)])
        return item

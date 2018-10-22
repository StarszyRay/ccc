# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv

class CccPipeline(object):

    def open_spider(self, spider):
        self.csvwriter = csv.writer(open('marki.csv', 'a'))
        self.csvwriter.writerow({'nazwa_marki', 'opis_marki'})
        self.ids_seen = set()
        self.markiT = []

    def close_spider(self, spider):
        for element in set(self.markiT):
            self.csvwriter.writerow([element[0], element[1]])
        pass

    def process_item(self, item, spider):
        self.markiT += (item['nazwa_marki'], item['opis_marki'])
        #self.csvwriter.writerow([item['nazwa_marki'],
        #                         item['opis_marki']])
        # self.csvwriter.writerow([item['ID'], item['zdjecia'],
        #                          item['nazwa'], item['indeks'],
        #                         item['kategoria'], item['cena'],
        #                         item['ilosc'], item['wyswietlany'],
        #                         item['pozycja']])
        return item

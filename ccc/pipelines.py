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

        if item['rozmiary'] == set():
            ilosc_rozmiarow = random.randint(2, 6)
            rozmiaryF = [32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42]
            rozmiaryM = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46]
            rozmiaryK = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]
            kat = item['kategoria']
            rozmiaryT = []
            if kat == 'f':
                rozmiaryT = rozmiaryF
            elif kat == 'm':
                rozmiaryT = rozmiaryM
            else:
                rozmiaryT = rozmiaryK
            rozmiary = []
            for a in range(ilosc_rozmiarow):
                rozmiar = random.choice(rozmiaryT)
                rozmiaryT.remove(rozmiar)
                rozmiary += [rozmiar]
            rozmiary = [str(r) for r in rozmiary]
            item['rozmiary'] = set(rozmiary)

        self.markiT.append((item['marka'], item['opis_marki'], item['zdjecie_marki'], item['wyswietlany']))
        if spider.name == 'obowie':
            for rozmiar in item['rozmiary']:
                if '/' not in rozmiar:
                    self.csv_kombinacje_writer.writerow(
                        [item['indeks'], "Rozmiar:select:0", "{0}:0".format(rozmiar), random.randint(10, 100)])
        return item

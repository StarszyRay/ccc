# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CccItem(scrapy.Item):
    indeks = scrapy.Field()
    zdjecia = scrapy.Field()
    nazwa = scrapy.Field()
    wyswietlany = scrapy.Field() #stale na 1
    kategoria = scrapy.Field()
    cena = scrapy.Field()
    ilosc = scrapy.Field()
    marka = scrapy.Field()
    opis_marki = scrapy.Field() #opdmienić przecinki na inny znak
    atrybuty = scrapy.Field() # nazwa:wartości;nazwa:wartosci;
    rozmiary = scrapy.Field()

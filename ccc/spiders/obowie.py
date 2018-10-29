# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ccc.items import CccItem
import random


class ObowieSpider(CrawlSpider):
    name = "obowie"
    allowed_domains = ["ccc.eu"]  # www.ccc.eu/pl
    start_urls = [
        # damskie
        "https://ccc.eu/pl/damskie/buty/botki",
        "https://ccc.eu/pl/damskie/buty/trzewiki",
        "https://ccc.eu/pl/damskie/buty/kozaki",
        "https://ccc.eu/pl/damskie/buty/czolenka",
        "https://ccc.eu/pl/damskie/buty/polbuty",
        "https://ccc.eu/pl/damskie/buty/sportowe",
        "https://ccc.eu/pl/damskie/buty/trampki",
        "https://ccc.eu/pl/damskie/buty/baleriny",
        "https://ccc.eu/pl/damskie/buty/espadryle",
        "https://ccc.eu/pl/damskie/buty/klapki-basenowe",
        "https://ccc.eu/pl/damskie/buty/kapcie",
        #meskie
        "https://ccc.eu/pl/meskie/buty/botki",
        "https://ccc.eu/pl/meskie/buty/trzewiki",
        "https://ccc.eu/pl/meskie/buty/polbuty",
        "https://ccc.eu/pl/meskie/buty/sportowe",
        "https://ccc.eu/pl/meskie/buty/trampki",
        "https://ccc.eu/pl/meskie/buty/klapki-basenowe",
        #dziewczece
        "https://ccc.eu/pl/dzieciece/dziewczece/botki",
        "https://ccc.eu/pl/dzieciece/dziewczece/trzewiki",
        "https://ccc.eu/pl/dzieciece/dziewczece/kozaki",
        "https://ccc.eu/pl/dzieciece/dziewczece/kalosze",
        "https://ccc.eu/pl/dzieciece/dziewczece/sportowe",
        "https://ccc.eu/pl/dzieciece/dziewczece/trampki",
        "https://ccc.eu/pl/dzieciece/dziewczece/polbuty",
        "https://ccc.eu/pl/dzieciece/dziewczece/kapcie",
        #chlopiece
        "https://ccc.eu/pl/dzieciece/chlopiece/trzewiki",
        "https://ccc.eu/pl/dzieciece/chlopiece/trzewiki",
        "https://ccc.eu/pl/dzieciece/chlopiece/kalosze",
        "https://ccc.eu/pl/dzieciece/chlopiece/sportowe",
        "https://ccc.eu/pl/dzieciece/chlopiece/polbuty",
        "https://ccc.eu/pl/dzieciece/chlopiece/trampki",
        "https://ccc.eu/pl/dzieciece/chlopiece/kapcie"
    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[contains(@href, "page=2")]',)),
             callback="parse_start_url",
             follow=True),)

    def parse_category(self, url):
        urlT = url.split("/")
        kategoria = urlT[-2]
        if "damskie" in urlT:
            kategoria = "f-" + kategoria.title()
        elif "meskie" in urlT:
            kategoria = "m-" + kategoria.title()
        elif "chlopiece" in urlT:
            kategoria = "b-" + kategoria.title()
        elif "dziewczece" in urlT:
            kategoria = "g-" + kategoria.title()
        elif "dzieciece" in urlT:
            kategoria = "k-" + kategoria.title()
        return (kategoria)

    def get_rozmiary1(self, response):
        item = response.meta['itemB']
        fixed_url = response.meta['fixed_url']
        rozmiary = response.xpath(
            '//div[@class="c-offerBox_hover"]/div/div[@class="c-offerBox_variantsContent"]/a[contains(@href, "' + fixed_url + '")]/text()').extract()
        rozmiary = [r.strip() for r in rozmiary]

        if not rozmiary:
            podkategoriaURL = response.url
            podkategoriaURL = podkategoriaURL + "?page=2"
            req = scrapy.Request(podkategoriaURL, callback=self.get_rozmiary2, dont_filter=True)
            req.meta['itemB'] = item
            req.meta['fixed_url'] = fixed_url
            return req
        else:
            item['rozmiary'] = set(rozmiary)
            return item

    def get_rozmiary2(self, response):
        item = response.meta['itemB']
        fixed_url = response.meta['fixed_url']
        rozmiary = response.xpath(
            '//div[@class="c-offerBox_hover"]/div/div[@class="c-offerBox_variantsContent"]/a[contains(@href, "' + fixed_url + '")]/text()').extract()
        rozmiary = [r.strip() for r in rozmiary]
        item['rozmiary'] = set(rozmiary)
        return item

    def parse_detail_page(self, response):
        item = CccItem()
        cenaT = response.css(".c-offerBox_col").css(".a-price span::text").extract()
        zdjeciaT = response.xpath('//div[@data-component="magnifier"]/img/@data-src').extract()
        zdjeciaT = ["https://ccc.eu{0}".format(zdjecie) for zdjecie in zdjeciaT]
        item["zdjecia"] = ';'.join(zdjeciaT)
        nazwa = response.css('.c-offerBox_data > .a-typo::text').extract()[0].strip()
        nazwa = nazwa.replace('&amp;', ' & ')
        item['nazwa'] = nazwa
        item['kategoria'] = self.parse_category(response.url)
        item['cena'] = cenaT[0] + '.' + cenaT[1]
        item['ilosc'] = random.randint(10, 100)
        item['wyswietlany'] = 1

        # marka + opis i zdjęcie
        item['marka'] = response.xpath('//table[@class="c-table is-specification"]/tbody/tr/td/span/text()').extract()[
            1].strip()
        item['opis_marki'] = ''
        item['zdjecie_marki'] = ''
        hint = response.css('.c-grid_row.is-about').css('div > p::text').extract()
        if hint != []:
            hint = hint[0]
            if hint.strip() == 'O marce':
                item['opis_marki'] = response.css('.c-grid_row.is-about').css('div > p::text').extract()[-1]
                link_zdj = response.css('div .c-content > div .widget.image_widget > a > img::attr(src)').extract_first()
                if link_zdj is not None:
                    item['zdjecie_marki'] = "https://ccc.eu{0}".format(link_zdj)

        # cechy
        cechyTrResponses = response.css('.c-table.is-specification').css('tr')
        cechyT = []
        for tr in cechyTrResponses:
            first = tr.css('span::text').extract_first().strip()
            second = tr.css('span::text').extract()
            second.pop(0)
            second = [s.strip() for s in second]
            second = [s.replace(',', '.') for s in second]
            second = ','.join(second)
            cechyT += [(first + ':' + second)]
            if first == "Kod produktu":
                item['indeks'] = second
        item['cechy'] = ';'.join(cechyT)

        # rozmiary
        podkategoriaURL = response.url
        while podkategoriaURL[-1] != '/':
            podkategoriaURL = podkategoriaURL[:-1]
        podkategoriaURL = podkategoriaURL[:-1]

        fixed_url = response.url
        fixed_url = fixed_url.split('/')[-1]
        fixed_url = fixed_url.split('-')[:-1]
        fixed_url = '-'.join(fixed_url)

        req = scrapy.Request(podkategoriaURL, callback=self.get_rozmiary1, dont_filter=True)
        req.meta['itemB'] = item
        req.meta['fixed_url'] = fixed_url
        return req

    def parse_start_url(self, response):
        item_links = response.xpath(
            '//div[@class="c-offerBox is-hovered"]/div[@class="c-offerBox_inner"]/div['
            '@class="c-offerBox_photo"]/a/@href').extract()
        for a in item_links:
            yield scrapy.Request('https://ccc.eu/' + a, callback=self.parse_detail_page, dont_filter=True)

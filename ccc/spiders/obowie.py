# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ccc.items import CccItem
import random


class ObowieSpider(CrawlSpider):
    name = "obowie"
    allowed_domains = ["ccc.eu"]    #www.ccc.eu/pl
    start_urls = [
        #damskie
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
        Rule(LinkExtractor(allow=(), restrict_css=(".is-next",)),
             callback="parse_item",
             follow=False),)

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
        return(kategoria)



    def parse_detail_page(self, response):
        item = CccItem()
        cenaT = response.css(".c-offerBox_col").css(".a-price span::text").extract()
        zdjeciaT = response.xpath('//div[@data-component="magnifier"]/img/@data-src').extract()
        zdjeciaT = ["https://ccc.eu{0}".format(zdjecie) for zdjecie in zdjeciaT]
        item["zdjecia"] = ';'.join(zdjeciaT)
        item['nazwa'] = response.css('.c-offerBox_data > .a-typo::text').extract()[0].strip()
        item['kategoria'] = self.parse_category(response.url)
        item['cena'] = cenaT[0] + '.' + cenaT[1]
        item['ilosc'] = random.randint(10, 100)
        item['wyswietlany'] = 1
        item['marka'] = response.xpath('//table[@class="c-table is-specification"]/tbody/tr/td/span/text()').extract()[1].strip()
        item['opis_marki'] = response.xpath('//div[@class="widget text_editor clearfix2"]/p/text()').extract_first()
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
        #cechy = ';'.join(cechyT)
        item['cechy'] = ';'.join(cechyT)
        #item['indeks'] = #response.css('.c-table.is-specification').css('tr').css('td').css('span::text').extract()[5].strip()
        #print(cechy)
        yield item
        #pass

    def parse_item(self, response):
        # item_links = response.css('.c-layout_col > .c-offerBox_photo a::attr(href)').extract()
        item_links = response.xpath('//div[@class="c-offerBox_inner"]/div[@class="c-offerBox_photo"]/a/@href').extract()
        for a in item_links:
            yield scrapy.Request('https://ccc.eu/' + a, callback=self.parse_detail_page)
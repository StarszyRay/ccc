# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ccc.items import CccItem
import random

class ObowieSpider(CrawlSpider):
    name = 'akcesoria'
    allowed_domains = ['ccc.eu']    #www.ccc.eu/pl
    start_urls = [
        #damskie
        'https://ccc.eu/pl/damskie/akcesoria/sznurowadla',
        'https://ccc.eu/pl/damskie/akcesoria/kosmetyki-do-obuwia',
        'https://ccc.eu/pl/damskie/akcesoria/szczotka',
        'https://ccc.eu/pl/damskie/akcesoria/wkladki-do-obuwia',
        #meskie
        'https://ccc.eu/pl/meskie/akcesoria/sznurowadla',
        'https://ccc.eu/pl/meskie/akcesoria/kosmetyki-do-obuwia',
        'https://ccc.eu/pl/meskie/akcesoria/szczotki',
        'https://ccc.eu/pl/meskie/akcesoria/wkladki-do-obuwia',
        #dzieciece
        'https://ccc.eu/pl/dzieciece/akcesoria/kosmetyki-do-obuwia',
        'https://ccc.eu/pl/dzieciece/akcesoria/sznurowadla'
    ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.is-next',)),
             callback="parse_item",
             follow=False),)

    def parse_category(self, url):
        urlT = url.split('/')
        kategoria = urlT[-2]
        if 'damskie' in urlT:
            kategoria = 'f-' + kategoria.title()
        elif 'meskie' in urlT:
            kategoria = 'm-' + kategoria.title()
        elif 'chlopiece' in urlT:
            kategoria = 'b-' + kategoria.title()
        elif 'dziewczece' in urlT:
            kategoria = 'g-' + kategoria.title()
        elif 'dzieciece' in urlT:
            kategoria = 'k-' + kategoria.title()
        return(kategoria)

    def parse_detail_page(self, response):
        item = CccItem()
        cenaT = response.css('.c-offerBox_col').css('.a-price span::text').extract()
        zdjeciaT = response.xpath('//div[@data-component="magnifier"]/img/@data-src').extract()
        zdjeciaT = ['https://ccc.eu{0}'.format(zdjecie) for zdjecie in zdjeciaT]
        item['zdjecia'] = ';'.join(zdjeciaT)
        item['nazwa'] = response.css('.c-offerBox_data > .a-typo::text').extract()[0].strip()
        item['kategoria'] = self.parse_category(response.url)
        item['cena'] = cenaT[0] + '.' + cenaT[1]
        item['ilosc'] = str(random.randint(100,200))
        item['marka'] = response.xpath('//table[@class="c-table is-specification"]/tbody/tr/td/span/text()').extract()[3].strip()
        item['opis_marki'] = '...'
        yield item

    def parse_item(self, response):
        #item_links = response.css('.c-layout_col > .c-offerBox_photo a::attr(href)').extract()
        item_links = response.css('.c-grid').xpath(
            '//div[@class="c-offerBox is-hovered"]/div[@class="c-offerBox_inner"]/div[@class="c-offerBox_photo"]/a/@href').extract()
        for a in item_links:
            yield scrapy.Request('https://ccc.eu/' + a, callback=self.parse_detail_page)
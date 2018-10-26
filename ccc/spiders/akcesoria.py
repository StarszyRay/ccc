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
             follow=True),)

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

    # def parse_detail_page(self, response):
    #     item = CccItem()
    #     cenaT = response.css('.c-offerBox_col').css('.a-price span::text').extract()
    #     zdjeciaT = response.xpath('//div[@data-component="magnifier"]/img/@data-src').extract()
    #     zdjeciaT = ['https://ccc.eu{0}'.format(zdjecie) for zdjecie in zdjeciaT]
    #     item['zdjecia'] = ';'.join(zdjeciaT)
    #     item['nazwa'] = response.css('.c-offerBox_data > .a-typo::text').extract()[0].strip()
    #     item['kategoria'] = self.parse_category(response.url)
    #     item['cena'] = cenaT[0] + '.' + cenaT[1]
    #     item['ilosc'] = str(random.randint(100,200))
    #     item['marka'] = response.xpath('//table[@class="c-table is-specification"]/tbody/tr/td/span/text()').extract()[3].strip()
    #     item['opis_marki'] = '...'
    #     yield item

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
        item['marka'] = response.xpath('//table[@class="c-table is-specification"]/tbody/tr/td/span/text()').extract()[
            1].strip()
        if response.xpath('//table[@class="c-table is-specification"]/tbody/tr/td/span/text()').extract()[
            0].strip() == 'Marka':
            item['marka'] = \
            response.xpath('//table[@class="c-table is-specification"]/tbody/tr/td/span/text()').extract()[
                1].strip()
        else:
            item['marka'] = \
            response.xpath('//table[@class="c-table is-specification"]/tbody/tr/td/span/text()').extract()[
                3].strip()
        # zdjecie_marki_path = response.xpath('//div[@class="widget image_widget"]/a/img[@alt="{0}"]/@src'.format(item['marka'])).extract()
        # if zdjecie_marki_path == []:
        #     item['zdjecie_marki'] = ''
        #     item['opis_marki'] = ''
        # else:
        #     item['opis_marki'] = response.xpath('//div[@class="widget text_editor clearfix2"]/p/text()').extract_first()
        #     item['zdjecie_marki'] = "https://ccc.eu{0}".format(zdjecie_marki_path)
        item['opis_marki'] = ''
        item['zdjecie_marki'] = ''
        hint = response.css('.c-grid_row.is-about').css('div > p::text').extract()
        if hint != []:
            hint = hint[0]
            if hint.strip() == 'O marce':
                item['opis_marki'] = response.css('.c-grid_row.is-about').css('div > p::text').extract()[-1]
                item['zdjecie_marki'] = "https://ccc.eu{0}".format(
                    response.css('div .c-content > div .widget.image_widget > a > img::attr(src)').extract_first()
                )
        ilosc_rozmiarow = random.randint(2, 5)
        rozmiaryT = [37, 38, 39, 40, 41, 42]
        rozmiary = []
        for a in range(ilosc_rozmiarow):
            rozmiar = random.choice(rozmiaryT)
            rozmiaryT.remove(rozmiar)
            rozmiary += [rozmiar]
        rozmiary = [str(r) for r in rozmiary]
        item['rozmiary'] = ','.join(rozmiary)
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
        # cechy = ';'.join(cechyT)
        item['cechy'] = ';'.join(cechyT)
        # item['indeks'] = #response.css('.c-table.is-specification').css('tr').css('td').css('span::text').extract()[5].strip()
        # print(cechy)
        yield item
        # pass

    def parse_item(self, response):
        item_links = response.xpath(
            '//div[@class="c-offerBox is-hovered"]/div[@class="c-offerBox_inner"]/div[@class="c-offerBox_photo"]/a/@href').extract()
        for a in item_links:
            # item_link = a.xpath('//div[@class="c-offerBox_inner"]/div[@class="c-offerBox_photo"]/a/@href').extract()
            # ROZMIARY = a.xpath('//div[@class="c-offerBox is-hovered"]/div/div/div[@class="c-offerBox_variantsContent"]').xpath('//div/a[@data-offer-id]/text()').extract()
            # print(ROZMIARY)
            # print('-----------------------------------------------------------------------')
            yield scrapy.Request('https://ccc.eu/' + a, callback=self.parse_detail_page)
            # pass
        #pass
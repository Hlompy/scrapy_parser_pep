import scrapy

from ..items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('a[href^="/pep-"]')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        data = {
            'number': int(response.css('h1.page-title::text').get().split('–')[0].split()[1]),
            'name': response.css('h1.page-title::text').get().split('–')[1],
            'status': response.css('dt:contains("Status") + dd::text').get(),
        }
        yield PepParseItem(data)

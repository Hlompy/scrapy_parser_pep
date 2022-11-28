import re
import scrapy

from pep_parse.items import PepParseItem

REG_EXPR = r'PEP\s(?P<number>\d+)\W+(?P<name>.+)$'


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        all_peps = response.css('a[href^="/pep-"]')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        h1 = response.css('h1.page-title::text').get()
        number, name = re.search(REG_EXPR, h1).groups()
        data = {
            'number': number,
            'name': name,
            'status': response.css('dt:contains("Status") + dd::text').get(),
        }
        yield PepParseItem(data)

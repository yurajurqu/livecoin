# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    url= "http://quotes.toscrape.com/js/"
    def start_requests(self):
        yield SplashRequest(url=self.url, callback=self.parse, endpoint="execute",
        args={
            'lua_source':self.script
        })

    def parse(self, response):
        for quote in response.xpath("//div[@class='quote']"):
            yield {
                'quote': quote.xpath(".//span[@class='text']/text()").get(),
                'author': quote.xpath(".//span[2]/small/text()").get(),
                'tags': quote.xpath(".//div[@class='tags']/a/text()").getall(),
            }

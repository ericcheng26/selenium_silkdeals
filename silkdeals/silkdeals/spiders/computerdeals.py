# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders.crawl import Rule, CrawlSpider


class ComputerdealsSpider(CrawlSpider):
    name = 'computerdeals'
    allowed_domains = ['slickdeals.net']
    # start_urls = ['https://slickdeals.net/computer-deals/']

    # def remove_characters(self, value):
    #     return value.strip('\xa0')
    

    def start_requests(self):
        yield SeleniumRequest(
            url='https://slickdeals.net/computer-deals/',
            wait_time=3
            # callback=self.parse
        )
    
    #!!!! 這段可以取代上面那段!! 一開始用scrapy.Request也抓得到，後來又嘗試了SeleniumRequest，發現也可以
    # def start_requests(self):
    #     yield scrapy.Request(
    #         url='https://slickdeals.net/computer-deals/'
    #         # wait_time=3
    #         # callback=self.parse
    #     )

    rules = (Rule(LinkExtractor(restrict_xpaths='//div[@class=\'itemImageLink\']/span/following-sibling::a'), callback='parse_item', follow=True),)


    def parse_item(self, response):
        yield{
            'prod_name':response.xpath("//div[@id='dealTitle']/h1/text()").get(),
            'price':response.xpath("//div[@class='dealPrice']/@title").get(),
            'prod_link':response.xpath("//div[@id='detailsDescription']/a/text()").get(),
            'description':response.xpath("//div[@id='detailsDescription']/text()").getall()

                # 'name':product.xpath(".//div[@class='itemImageLink']/a/text()").get(),
                # 'link':response.urljoin(product.xpath(".//div[@class='itemImageLink']/a/@href").get()),
                # 'store_name':product.xpath(".//div[@class='itemImageLink']/a/text()").get(),
                # 'price':product.xpath(".//div[@class='itemPrice  wide ']/text()").get()
        }

        next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            absolute_url = f"https://slickdeals.net{next_page}"
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=3,
                callback=self.parse
            )
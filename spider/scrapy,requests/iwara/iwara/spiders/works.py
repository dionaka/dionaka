import scrapy
import requests
from iwara.items import IwaraItem

class WorksSpider(scrapy.Spider):
    name = "works"
    allowed_domains = ["www.iwara.tv"]
    start_urls = ["https://api.iwara.tv/search?type=video&page=0&query=%E5%8E%9F%E7%A5%9E"]

    def parse(self, response):
        dom_list=response.xpath("//div[@class='text text--text text--bold']")
        for dom in dom_list:
            name=dom.xpath('font/font/text()').extract_first()

            IwaraItem["name"]=name
            yield IwaraItem()

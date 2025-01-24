import scrapy
from qidian_hot.items import QidianHotItem
class HotsaleSpider(scrapy.Spider):
    name='hot'

    start_urls=["https://www.qidian.com/rank/hotsales/"]

    def parse(self,response):
       list_selector=response.xpath("//li/div[@class='book-mid-info']")
       for one_selector in list_selector:
            item = QidianHotItem()
            name=one_selector.xpath("./h2/a/text()").extract_first()
            author=one_selector.xpath("./p[1]/a[1]/text()").extract_first()
            type=one_selector.xpath("./p[1]/a[2]/text()").extract_first()
            form=one_selector.xpath("./p[1]/span/text()").extract_first()

            item['name']=name
            item['author']=author
            item['type']=type
            item['form']=form
            yield item


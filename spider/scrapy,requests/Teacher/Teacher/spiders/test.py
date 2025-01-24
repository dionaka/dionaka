import scrapy
from Teacher.items import TeacherItem


class TestSpider(scrapy.Spider):
    name = "test"
    allowed_domains = ["www.itcast.cn"]
    start_urls = ["https://www.itheima.com/teacher.html"]

    def parse(self, response):
        node_list=response.xpath("//div[@class='li_txt']")
        items=[]
        for node in node_list:
            item = TeacherItem()

            name=node.xpath("./h3/text()").extract_first()
            title=node.xpath("./h4/text()").extract_first()
            info=node.xpath("./p/text()").extract_first()

            item['name']=name
            item['title']=title
            item['info']=info
            items.append(item)
        return items

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TeacherItem(scrapy.Item):
    #姓名
    name = scrapy.Field()
    #简历
    title = scrapy.Field()
    #职业
    info = scrapy.Field()
    #pass

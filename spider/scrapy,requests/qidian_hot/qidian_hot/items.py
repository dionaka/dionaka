# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QidianHotItem(scrapy.Item):
    name = scrapy.Field()
    author = scrapy.Field()
    type = scrapy.Field()
    form=scrapy.Field()

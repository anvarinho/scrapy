# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FranchItem(scrapy.Item):
    # define the fields for your item here like:
    rank = scrapy.Field()
    name = scrapy.Field()
    country = scrapy.Field()
    industry = scrapy.Field()
    year = scrapy.Field()
    url = scrapy.Field()
    # total = scrapy.Field()
    # fee = scrapy.Field()
    

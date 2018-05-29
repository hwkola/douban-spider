# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MoviesItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    directors = scrapy.Field()
    rating_count = scrapy.Field()
    rating_value = scrapy.Field()
    tags = scrapy.Field()
    year = scrapy.Field()
    url = scrapy.Field()
    casts = scrapy.Field()
    cover = scrapy.Field()
    short_info = scrapy.Field()
    desc = scrapy.Field()




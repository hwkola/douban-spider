# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, replace_escape_chars


class FirstItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MoviesItem(scrapy.Item):
    collection = 'movies'
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
    crawled_at = scrapy.Field()


class BooksItem(scrapy.Item):
    collection = 'books'
    id = scrapy.Field()
    url = scrapy.Field()        # 网页地址
    title = scrapy.Field()      # 书名
    author = scrapy.Field(input_processor=MapCompose(remove_tags, replace_escape_chars))     # 作者
    publisher = scrapy.Field(input_processor=MapCompose(replace_escape_chars))      # 出版社
    producer = scrapy.Field(input_processor=MapCompose(replace_escape_chars))       # 出品方
    org_name = scrapy.Field()       # 原作名
    translators = scrapy.Field()        # 译者
    publish_year = scrapy.Field(input_processor=MapCompose(replace_escape_chars))       # 出版年
    page_num = scrapy.Field(input_processor=MapCompose(replace_escape_chars))       # 页数
    price = scrapy.Field(input_processor=MapCompose(replace_escape_chars))      # 定价
    framed = scrapy.Field(input_processor=MapCompose(replace_escape_chars))     # 装帧
    series = scrapy.Field()
    subtitle = scrapy.Field()
    isbn = scrapy.Field()
    cover_path = scrapy.Field()
    rating_num = scrapy.Field()     # 评分
    rating_people = scrapy.Field()      # 评价人数
    desc = scrapy.Field(input_processor=MapCompose(remove_tags, replace_escape_chars))       # 简介
    contents = scrapy.Field(input_processor=MapCompose(replace_escape_chars))       # 目录
    crawled_at = scrapy.Field()


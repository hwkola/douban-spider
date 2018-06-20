# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem

from .items import MoviesItem, BooksItem
from scrapy.pipelines.images import ImagesPipeline


class DoubanPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri=crawler.settings.get('MONGO_URI'),
                   mongo_db=crawler.settings.get('MONGO_DATABASE'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[MoviesItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[BooksItem.collection].create_index([('id', pymongo.ASCENDING)])

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, MoviesItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        if isinstance(item, BooksItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)
        return item['title']


class ImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Download Field')
        return item

    def get_media_requests(self, item, info):
        yield Request(url=item['cover_path'])


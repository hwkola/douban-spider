# -*- coding: utf-8 -*-
import json
import re
import time

from ..items import MoviesItem
import scrapy


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['movie.douban.com', 'm.douban.com']
    start_urls = ['https://movie.douban.com/']
    range_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range={0},{1}&tags=&start={2}'
    movie_url = 'https://m.douban.com/rexxar/api/v2/elessar/subject/{mid}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }

    custom_settings = {
        # Redis配置
        'SCHEDULER': 'scrapy_redis.scheduler.Scheduler',
        'DUPEFILTER_CLASS': 'scrapy_redis.dupefilter.RFPDupeFilter',
        'SCHEDULER_PERSIST': False   # 配置强制结束爬虫后, 销毁爬虫的相关key, 测试方便
    }

    def parse_movie(self, response):
        """
        解析影片详情
        :param response:
        :return:
        """
        rest = json.loads(response.text)
        if rest.get('id'):
            movie_item = MoviesItem()
            field_map = {
                'id': 'id', 'year': 'year', 'short_info': 'short_info'
            }
            for f, a in field_map.items():
                movie_item[f] = rest.get(a)
            movie_item['year'] = rest.get('extra').get('year')
            movie_item['short_info'] = rest.get('extra').get('short_info')
            movie_item['desc'] = re.match('^<[\s\S]*>([\s\S]*)</div>', rest.get('desc')).group(1)    # 清洗desc
            movie_item['rating_count'] = rest.get('extra').get('rating_group').get('rating').get('count')
            movie_item['rating_value'] = rest.get('extra').get('rating_group').get('rating').get('value')
            movie_item['tags'] = [i['name'] for i in rest.get('tags')]   # 清洗tags, 只保留名称
            movie_item['crawled_at'] = time.strftime('%Y-%m-%d %H:%M', time.localtime())    # 添加爬取日期

            yield movie_item

    def parse(self, response):
        """
        分析通过评分API获取的影片
        :param response:
        :return:
        """
        rest = json.loads(response.text)
        if len(rest.get('data')) > 0:
            items = rest.get('data')
            movie_item = MoviesItem()
            for i in items:
                field_map = {
                    'id': 'id', 'title': 'title', 'url': 'url',
                    'casts': 'casts', 'cover': 'cover', 'directors': 'directors',
                }
                for f, a in field_map.items():
                    movie_item[f] = i.get(a)
                yield movie_item

                # 请求影片M站API
                mid = i.get('id')
                yield scrapy.Request(self.movie_url.format(mid=mid), headers=self.headers, callback=self.parse_movie)

        # "加载更多"的请求
        start = response.meta.get('start') + 20
        r = response.meta.get('r')
        yield scrapy.Request(url=self.range_url.format(r[0], r[1], start), headers=self.headers, callback=self.parse,
                             meta={'r': r, 'start': start})

    def start_requests(self):
        """
        轮询请求各评分区的API
        :return:
        """
        range_map = ((8, 10), (5, 7), (0, 5))
        for r in range_map:
            yield scrapy.Request(url=self.range_url.format(r[0], r[1], 0), headers=self.headers,
                                 meta={'r': r, 'start': 0})





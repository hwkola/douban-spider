# -*- coding: utf-8 -*-
import json
from ..items import MoviesItem
import scrapy


class MoviesSpider(scrapy.Spider):
    name = 'movies'
    allowed_domains = ['movie.douban.com', 'm.douban.com']
    start_urls = ['https://movie.douban.com/']
    range_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range={0},{1}&tags=&start={2}'
    movie_url = 'https://m.douban.com/rexxar/api/v2/elessar/subject/{mid}'

    w_headers = {
        "HOST": 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
    }

    m_headers = {
        "HOST": 'm.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
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
                'year': 'year', 'short_info': 'short_info', 'desc': 'desc'
            }
            for f, a in field_map.items():
                movie_item[f] = rest.get(a)
            movie_item['rating_count'] = rest.get('extra').get('rating_group').get('rating').get('count')
            movie_item['rating_value'] = rest.get('extra').get('rating_group').get('rating').get('value')
            movie_item['tags'] = [i['name'] for i in rest.get('tags')]

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
                yield scrapy.Request(self.movie_url.format(mid=mid), headers=self.m_headers, callback=self.parse_movie)

        # "加载更多"的请求
        start = response.meta.get('start') + 20
        r = response.meta.get('r')
        yield scrapy.Request(url=self.range_url.format(r[0], r[1], start), headers=self.w_headers, callback=self.parse,
                             meta={'r': r, 'start': start})

    def start_requests(self):
        """
        轮询请求各评分区的API
        :return:
        """
        range_map = ((8, 10), (5, 7), (0, 5))
        for r in range_map:
            yield scrapy.Request(url=self.range_url.format(r[0], r[1], 0), headers=self.w_headers,
                                 meta={'r': r, 'start': 0})





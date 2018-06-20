# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from ..common import get_md5, value_to_dict
from ..items import FirstItemLoader, BooksItem
from datetime import datetime


class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['book.douban.com', 'img3.doubanio.com', 'img1.doubanio.com', 'img2.doubanio.com']
    start_urls = ['https://book.douban.com/subject/30155720/']

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810},
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100},
        'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
        'DOWNLOAD_DELAY': 1,
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        },
        'ITEM_PIPELINES': {
            'douban.pipelines.ImagePipeline': 300,
            'douban.pipelines.MongoPipeline': 302},
        'IMAGES_STORE': './images/books/'
    }

    def parse(self, response):
        i = FirstItemLoader(item=BooksItem(), response=response)
        i.add_value('id', get_md5(response.url))
        i.add_value('url', response.url)
        i.add_css('title', '#wrapper h1 span::text')
        info = Selector(response).css('#info').extract_first()
        info = value_to_dict(info)
        field_map = {
            '作者': 'author', '出品方': 'publisher', '原作名': 'org_name', '译者': 'translators',
            '出版年': 'publish_year', '页数': 'page_num',  '定价': 'price', '装帧': 'framed',
            'ISBN': 'isbn', '出版社': 'publisher', '丛书': 'series', '副标题': 'subtitle'}
        for k, v in info.items():
            i.add_value(field_map[k], v)
        i.add_css('cover_path', '.nbg::attr(href)')
        i.add_css('rating_num', 'strong[class="ll rating_num "]::text')
        i.add_css('rating_people', '.rating_people span::text')
        i.add_xpath('desc', '//*[@id="link-report"]/span/div[1]')
        i.add_css('contents', '.related_info div:nth-child(4)::text')
        i.add_value('crawled_at', datetime.now())

        book_item = i.load_item()

        yield book_item

        # 根据页面的喜欢读... 提取其他书籍链接, 追踪爬取
        urls = Selector(response).css('#db-rec-section div dl dt a::attr(href)').extract()
        for url in urls:
            yield SplashRequest(url, self.parse, args={'wait': 2})

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2})


# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals


class TrainprojectSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TrainprojectDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        proxy = self.get_proxy()
        print("this is request ip:" + proxy)
        request.meta['proxy'] = proxy
        return None

    def process_response(self, request, response, spider):
        if response.status != 200:
            proxy = self.get_proxy()
            print("change another ip:" + proxy)
            request.meta['proxy'] = proxy
            return request
        return response

    def process_exception(self, request, exception, spider):
        pass

    def get_proxy(self):
        import redis
        import random

        pool = redis.ConnectionPool(host='210.73.194.41', port=16379, password='Jz123456', db=10)
        r = redis.StrictRedis(connection_pool=pool)
        cont = r.lrange('server1', 1000, 30000)
        ippool = []
        for i, val in enumerate(cont):
            ip = "http://" + str(cont[i].decode('utf8'))
            ippool.append(ip)
        proxy = random.choice(ippool).strip()
        return proxy

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

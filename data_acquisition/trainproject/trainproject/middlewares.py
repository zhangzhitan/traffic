# -*- coding: utf-8 -*-
from scrapy import signals
import data_acquisition.trainproject.redis_setting as rcfg


class TrainprojectSpiderMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):

        return None

    def process_spider_output(self, response, result, spider):

        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):

        pass

    def process_start_requests(self, start_requests, spider):

        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TrainprojectDownloaderMiddleware(object):


    @classmethod
    def from_crawler(cls, crawler):

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

        pool = redis.ConnectionPool(host=rcfg.REDIS_HOST, port=rcfg.REDIS_POST, password=rcfg.REDIS_PASSWORD, db=10)
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

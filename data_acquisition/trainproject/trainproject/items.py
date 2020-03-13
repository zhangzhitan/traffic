# -*- coding: utf-8 -*-
import scrapy


class TrainprojectItem(scrapy.Item):

    realtrainnum = scrapy.Field()
    arrtime = scrapy.Field()
    deptime = scrapy.Field()
    code = scrapy.Field()
    statianname = scrapy.Field()
    delayflag = scrapy.Field()
    delaydetail = scrapy.Field()
    results = scrapy.Field()

    pass

# -*- coding: utf-8 -*-
import pymssql
import datetime
from scrapy.conf import settings

class TrainprojectPipeline(object):

    def __init__(self):
        self.conn = pymssql.connect(host='YOURHOST', port='YOURPORT', user='YOURUSER', password='YOURPASSWORD',
                                    database='Train', charset='utf8')
        self.offset = 0
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        firstStep = datetime.datetime.now() - datetime.timedelta(3)
        targetDate = str(firstStep)[0:10]
        date = targetDate[0:4] + targetDate[5:7] + targetDate[8:10]
        realtrainnum = str(item.get("realtrainnum", "- -"))
        arrtime = item.get("arrtime", "- -")
        deptime = item.get("deptime", "- -")
        code = item.get("code", "- -")
        statianname = item.get("statianname", "- -")
        delayflag = item.get("delayflag", "- -")
        delaydetail = str(item.get("delaydetail", "- -"))
        sql = "insert into newtrain{}(realtrainnum, arrtime, deptime, code, stationname, delayflag, delaydetail) VALUES (%s, %s, %s, %s, %s, %s, %s)".format(date)
        self.cursor.execute(sql, (realtrainnum, arrtime, deptime, code, statianname, delayflag, delaydetail))
        self.conn.commit()
        return item

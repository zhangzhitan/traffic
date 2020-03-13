# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import datetime
import random
import json
import redis  # 问题在于anaconda里面有redis,但是为了import 正确需要再安装redis-py
import time
import data_acquisition.trainproject.items as items


class TraincrawlerSpider(scrapy.Spider):
    name = 'traincrawler'

    def start_requests(self):
        firstStep = datetime.datetime.now() - datetime.timedelta(3)
        targetDate = str(firstStep)[0:10]
        pool = redis.ConnectionPool(host='XXXXX', port=16379, password='XXXX', db=XX, decode_responses=True)
        r = redis.StrictRedis(connection_pool=pool, decode_responses=True)
        today = random.randint(0, 40)
        combinations = r.lrange('uid.{}'.format(str(today)), 1, -1)  # 这时候cont是一个字符串列表



        userAgents = [
            # Apple iPhone XR (Safari)
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1",
            # Apple iPhone XS (Chrome)
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1",
            # Apple iPhone XS Max (Firefox)
            "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15",
            # Apple iPhone X
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            # Apple iPhone 8
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1",
            # Apple iPhone 8 Plus
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1"
        ]
        userAgent = random.choice(userAgents)
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "Origin": "https://h5.133.cn",
            "User-Agent": userAgent,
        }

        forbidden_api = "https://jp.rsscc.com/gateway/gtgj/dyn"

        threeCharacterCode = pd.read_csv("C://traincode.csv")
        for row in threeCharacterCode.itertuples(index=False, name='Pandas'):
            departDate = targetDate
            trainNo = getattr(row, "num")
            departCode = getattr(row, "dep")
            arriveCode = getattr(row, "arr")
            combination = random.choice(combinations)
            info = json.loads(combination)
            uid = info['uid']
            sid = info['sid']
            form_data = {
                'client': 'vuetrainweb',
                'source': 'vuetrainweb',
                'platform': 'web',
                'cver': '7.0',
                'dver': '0',
                'iver': '5.32',
                'format': 'json',
                'uid': uid,
                'imei': uid,
                'uuid': uid,
                'p': 'vuetrainweb,ios,vuetrainweb,7.0,web',
                'appinfo': 'vuetrainweb,ios,vuetrainweb,7.0,web',
                'pid': '331553',
                'departDate': '{}'.format(targetDate),
                'trainNo': '{}'.format(trainNo),
                'departCode': '{}'.format(departCode),
                'arriveCode': '{}'.format(arriveCode),
                'sid': sid
            }
            time.sleep(2)
            yield scrapy.FormRequest(url=forbidden_api, formdata=form_data, headers=headers)

    def parse(self, response):
        item = items.TrainprojectItem()
        import json
        original = json.loads(response.text)
        print(original)
        try:
            successfulflag = original['res']['hd']['desc']
            if successfulflag == "success":
                print("请求成功")
            elif successfulflag == "请求参数错误":
                print("请求参数错误")
            elif successfulflag == "时刻信息已过期":
                print("时刻信息已过期")
            elif  successfulflag == "网络请求处理失败":
                print("网络请求处理失败")
            elif successfulflag == "数据异常,请确认客户端版本":
                print("数据异常,请确认客户端版本")
            else:
                print("列车号错误或者管家暂未收录该列车时刻信息")
        except:
            print("请求头解析失败，确认爬虫是否被高铁管家发现")

        results = original['res']['bd']['data']['stationList']
        realtrainnum = results[0]['rtn']
        for result in results:
            try:
                # 如果出发与到达的时间段为空，则出发与到达日期不存在
                if result['dt'] != '':
                    deptime = result['dd'] + ' ' + result['dt']
                else:
                    deptime = 'end'
                if result['at'] != '':
                    arrtime = result['ad'] + ' ' + result['at']
                else:
                    arrtime = 'start'
                code = result['c']
                statianname = result['n']
                try:
                    if result['zwd']['z'] == 1:
                        delayflag = "正点"
                    elif result['zwd']['z'] == 2:
                        delayflag = "提前"
                    else:
                        delayflag = "晚点"
                    delaydetail = result['zwd']['dl']
                except:
                    delayflag = "缺失"
                    delaydetail = '-'
                print(realtrainnum, arrtime, deptime, code, statianname, delayflag, delaydetail)
                item['realtrainnum'] = realtrainnum
                item['arrtime'] = arrtime
                item['deptime'] = deptime
                item['code'] = code
                item['statianname'] = statianname
                item['delayflag'] = delayflag
                item['delaydetail'] = delaydetail
                print("数据转载完成，准备传输")
                yield item
            except:
                print("解析失败")
                continue
#!/usr/bin/python3
# -*- coding: utf-8 -*-
import pymssql
import datetime
import data_processing.database_setting as cfg


def gen_time_list(start_date, end_date, format_type):

    """
    输入起始日期与终止日期，循环执行SQL语句
    :param start_date: 起始日期
    :param end_date: 终止日期
    :return: 格式化日期列表
    """
    start = datetime.datetime.strptime(start_date, format_type)
    end = datetime.datetime.strptime(end_date, format_type)
    date_list = []
    while end > start:
        date_list.append(datetime.datetime.strftime(start, format_type)[:10])
        start += datetime.timedelta(1)

    return date_list


if __name__ == '__main__':

    dts = gen_time_list('20190701', '20201231', "%Y%m%d")
    conn = pymssql.connect(host=cfg.TRAIN_HOST, port=cfg.TRAIN_PORT, user=cfg.TRAIN_USER, password=cfg.TRAIN_PASSWORD,
                           database=cfg.TRAIN_DATABASE, charset='utf8')
    cursor = conn.cursor()

    SQL = '''create table transform{}(realtrainnum nvarchar(30), lastarrtime nvarchar(30), 
    thisdeptime nvarchar(30), thisdepcode nvarchar(10),thisarrtime nvarchar(30), nextdeptime nvarchar(30),
    thisarrcode nvarchar(30), delayflag nvarchar(30), delaydetail nvarchar(30), rownum nvarchar(20), allrow nvarchar(30))'''
    for date in dts:
        cursor.execute(SQL.format(date))
        print(SQL.format(date))
        conn.commit()

    conn.close()

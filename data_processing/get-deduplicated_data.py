#!/usr/bin/python3
# -*- coding: utf-8 -*-
__Author__ = 'zhang zhitan'
__Author_email__ = 'z.zhitan@foxmail.com'
__copyright__ = 'copyright 2020 zhang zhitan'

import pymssql
import pandas as pd
import datetime
import data_processing.database_setting as cfg

def get_pure_data(start_date, end_date, file_path):

    """
    传入起始日期与终止日期，及希望保存的文件路径
    建议保存成cs格式，Excel 数据量过大可能导出失败
    :return:  返回到本地的一个文件
    """

    conn = pymssql.connect(host=cfg.TRAIN_HOST, port=cfg.TRAIN_PORT, user=cfg.TRAIN_USER, password=cfg.TRAIN_PASSWORD,
                            database=cfg.TRAIN_DATABASE, charset='utf8')
    cursor = conn.cursor()

    create_view_sql = "EXEC create_interval '{}','{}'".format(start_date, end_date)
    cursor.execute(create_view_sql)
    conn.commit()

    read_table_sql = 'SELECT realtrainnum,arrtime,deptime,code,stationname,delayflag,delaydetail FROM temp_query WHERE id_num IN (SELECT MAX(id_num) FROM temp_query GROUP BY arrtime,deptime,code,dropflag)'
    original_df = pd.read_sql(read_table_sql, conn)
    conn.close()

    pd.set_option('display.max_columns', 20)
    pd.set_option('display.width', 2000)
    pd.set_option('display.max_rows', 100)
    original_df.to_csv(file_path, index=None)


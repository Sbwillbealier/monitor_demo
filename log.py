#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/23
@file:log.py
@desc: 统计变化数据的日志
"""
import time
import datetime
from app.tools.monitor import Monitor
from app.models.models import Cpu, Swap, Mem
from app.tools.orm import ORM


def dt():
    """日期函数"""
    dt = datetime.datetime.now()
    _date_time = dt.strftime("%Y-%m-%d %H:%M:%S")
    _date = dt.strftime("%Y-%m-%d")
    _time = dt.strftime("%H:%M:%S")
    return _date_time, _date, _time


def save_log():
    """保存日志的函数"""
    m = Monitor()
    cpu_info, swap_info, mem_info = m.cpu(), m.swap(), m.mem()
    _date_time, _date, _time = dt()
    # 1.创建会话
    session = ORM.db()
    try:
        # cpu
        cpu = Cpu(
            percent=cpu_info['percent_avg'],
            create_date=_date,
            create_time=_time,
            create_dt=_date_time,
        )
        # 交换分区
        swap = Swap(
            percent=swap_info['percent'],
            total=swap_info['total'],
            used=swap_info['used'],
            free=swap_info['free'],
            create_date=_date,
            create_time=_time,
            create_dt=_date_time,
        )
        # 内存
        mem = Mem(
            percent=mem_info['percent'],
            total=mem_info['total'],
            used=mem_info['used'],
            free=mem_info['free'],
            create_date=_date,
            create_time=_time,
            create_dt=_date_time,
        )

        # 提交至数据库
        session.add(cpu)
        session.add(swap)
        session.add(mem)
    except Exception as e:
        session.rollback()  # 出错回滚
        print('出错回滚:{}'.format(e))
    else:
        session.commit()  # 正常，提交
        print('正常，提交')
    finally:
        session.close()  # 关闭会话
        print('关闭会话')


if __name__ == '__main__':
    while True:
        _date_time, _, _ = dt()
        print('开始时间：{}'.format(_date_time))
        save_log()
        print('结束时间：{}'.format(_date_time))
        time.sleep(60)

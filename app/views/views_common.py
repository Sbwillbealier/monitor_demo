#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/19
@file:views_common.py
@desc: 自定义视图函数的基类，添加方法，使其不同范围的值返回不同的颜色
"""

import tornado.web
from app.tools.monitor import Monitor


class CommonHandler(tornado.web.RequestHandler):
    """通用视图函数"""

    def progress_status(self, value):
        """进度条状态"""
        if 0 <= value < 25:
            data = "bg-success"  # 绿色
        elif value < 50:
            data = ""  # 默认
        elif value < 75:
            data = "bg-warning"  # 橙色
        elif value <= 100:
            data = "bg-danger"  # 红色

        return data

    @property
    def started(self):
        """开机时间"""
        m = Monitor()
        return m.get_last_boot()

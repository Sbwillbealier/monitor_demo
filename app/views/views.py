#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/13
@file:views.py
@desc: 定义视图函数（handler）
"""
import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    """首页视图"""

    def get(self):
        self.write('<h1>硬件实时监控系统</h1>')

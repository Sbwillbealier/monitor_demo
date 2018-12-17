#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/5
@file:urls.py
@desc: 路由规则
"""
from app.views.views_index import IndexHandler
from sockjs.tornado import SockJSRouter  # socket专用路由类
from app.views.view_real_time import RealTimeHandler

urls = [
           ('/', IndexHandler),
       ] + SockJSRouter(RealTimeHandler, '/real/time').urls

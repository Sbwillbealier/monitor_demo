#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/5
@file:configs.py
@desc: 配置信息
"""
import os

configs = dict(
    debug=True,  # 开启调试模式
    template_path=os.path.join(os.path.dirname(__file__), 'templates'),
    static_path=os.path.join(os.path.dirname(__file__), 'static'),
)

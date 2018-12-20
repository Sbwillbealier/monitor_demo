#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/13
@file:views.py
@desc: 定义视图函数（handler）
"""
from app.tools.chart import Chart
from app.tools.monitor import Monitor
from app.views.views_common import CommonHandler


class IndexHandler(CommonHandler):
    """首页视图"""

    def get(self):
        # self.write('<h1>硬件实时监控系统</h1>')
        m = Monitor()
        cpu_info = m.cpu()
        mem_info = m.mem()
        swap_info = m.swap()

        c = Chart()
        self.render('index.html', data=dict(
            cpu_liquid=c.liquid_html('cpu_avg', 'CPU平均使用率', cpu_info['percent_avg']),
            cpu_info=cpu_info,
            mem_gauge=c.gauge_html('mem', '内存使用率', mem_info['percent']),
            mem_info=mem_info,
            swap_gauge=c.gauge_html('swap', '交换分区使用率', swap_info['percent']),
            swap_info=swap_info,
        ))

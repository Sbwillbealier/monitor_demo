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
        c = Chart()  # 生成图对象
        m = Monitor()  # 获取系统信息对象
        # CPU信息
        cpu_info = m.cpu()

        # 内存信息
        mem_info = m.mem()

        # 交换分区信息
        swap_info = m.swap()

        # 网络信息
        net_info = m.net()
        net_pie = [
            c.pie_two_html(
                chart_id="net{}".format(k + 1),
                title="{}网卡信息".format(v['name']),
                sub_title1='收发包数统计',
                sub_title2='收发字节统计',
                key1=['收包数', '发包数'],
                value1=[v['packets_recv'], v['packets_sent']],
                key2=['收字节数', '发字节数'],
                value2=[v['bytes_recv'], v['bytes_sent']]
            )
            for k, v in enumerate(net_info) if v['packets_recv'] and v['packets_sent']
        ]

        self.render('index.html', data=dict(
            cpu_liquid=c.liquid_html('cpu_avg', 'CPU平均使用率', cpu_info['percent_avg']),
            cpu_info=cpu_info,
            mem_gauge=c.gauge_html('mem', '内存使用率', mem_info['percent']),
            mem_info=mem_info,
            swap_gauge=c.gauge_html('swap', '交换分区使用率', swap_info['percent']),
            swap_info=swap_info,
            net_pie=net_pie,
            net_info=net_info,
        ))

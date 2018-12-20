#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/17
@file:chart.py
@desc: pyecharts制作部分
"""
from pyecharts import Liquid, Gauge
import datetime


class Chart(object):
    """制作图标"""

    def liquid_html(self, chart_id, title, val):
        """CPU水球图"""
        # 实例一个具体类型图表的对象,并配置基本项
        liquid = Liquid(
            title="{}-{}".format(self.dt, title),
            title_pos='center',
            width='100%',
            title_color='white',
            title_text_size=14,
            height=300
        )

        # 绑定id
        liquid.chart_id = chart_id

        # 绑定参数
        liquid.add("", [round(val / 100, 4)])

        return liquid.render_embed()  # 返回图表html代码

    def gauge_html(self, chart_id, title, val):
        """内存、交换分区仪表图"""
        gauge = Gauge(
            "{}-{}".format(self.dt, title),
            title_pos="center",
            width="100%",
            title_text_size=14,
            title_color="white",
            height=300
        )
        gauge.chart_id = chart_id
        gauge.add(
            "",
            "",
            val,
            scale_range=[0, 100],
            is_legend_show=False
        )
        return gauge.render_embed()

    @property
    def dt(self):
        """返回当前日期"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

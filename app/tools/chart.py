#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/17
@file:chart.py
@desc: pyecharts制作部分
"""
from pyecharts import Liquid, Gauge, Pie, Line
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

    def pie_two_html(self, chart_id, title, sub_title1, sub_title2, key1, value1, key2, value2):
        """网络信息双饼图"""
        pie = Pie(
            title="{}-{}".format(self.dt, title),
            title_pos='center',
            width='100%',
            height=300,
            title_text_size=14,
            title_color='white'
        )
        # 指定id
        pie.chart_id = chart_id
        # 添加数据
        pie.add(
            name=sub_title1,
            attr=key1,
            value=value1,
            center=[25, 50],
            is_random=True,
            radius=[30, 75],
            rosetype="radius",
            is_legend_show=True,
            is_label_show=True,
            label_text_size=15,
            legend_text_size=14,
        )
        pie.add(
            name=sub_title2,
            attr=key2,
            value=value2,
            center=[65, 50],
            is_random=True,
            radius=[30, 75],
            rosetype="radius",
            is_legend_show=True,
            is_label_show=True,
            legend_pos="right",
            legend_orient="vertical",
            label_text_size=15
        )
        return pie.render_embed()

    def line_html(self, title, key, val, color=None):
        """折线面积图"""
        line = Line(
            title,
            title_pos='center',
            width='100%',
            height=300,
        )
        line.add(
            "",
            key,
            val,
            is_fill=True,  # 是否填充曲线面积
            mark_point=['average', 'max', 'min'],  # 标记点
            mark_line=['average'],  # 标记线
            line_opacity=0.2,
            area_opacity=0.4,
            is_datazoom_show=True,  # 缩放
            datazoom_range=[0, 100],
            symbol=None,  # 标记图形
            area_color=color,
        )

        return line.render_embed()

    def line_three_html(self, title, key, val_min, val_max, val_avg):
        """折线面积图"""
        line = Line(
            title,
            title_pos='left',
            width='100%',
            height=300,
        )
        line.add(
            "最小值",
            key,
            val_min,
            mark_point=['average', 'max', 'min'],  # 标记点
            is_datazoom_show=True,  # 缩放
            datazoom_range=[0, 100],
            is_smooth=True,
        )
        line.add(
            "最大值",
            key,
            val_max,
            mark_point=['average', 'max', 'min'],  # 标记点
            is_datazoom_show=True,  # 缩放
            datazoom_range=[0, 100],
            is_smooth=True,
        )
        line.add(
            "平均值",
            key,
            val_avg,
            mark_point=['average', 'max', 'min'],  # 标记点
            is_datazoom_show=True,  # 缩放
            datazoom_range=[0, 100],
            is_smooth=True,
        )

        return line.render_embed()

    @property
    def dt(self):
        """返回当前日期"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

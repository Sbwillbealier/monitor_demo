#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/23
@file:views_log.py
@desc: 日志视图函数
"""
import datetime
from app.views.views_common import CommonHandler
from sqlalchemy import and_, func
from app.tools.orm import ORM
from app.models.models import Cpu, Swap, Mem
from app.tools.chart import Chart


class LogHandler(CommonHandler):
    """"""

    def get(self):
        data = dict(
            title='日志统计'
        )

        # 用id表示1小时， 1天， 1月
        id = self.get_argument('id')
        c = Chart()

        # 1小时
        if int(id) == 1:
            attr_cpu, attr_swap, attr_mem, vals_cpu, vals_swap, vals_mem = self.data_by_hour()

            # cpu折线图
            if attr_cpu and vals_cpu:
                data['line_cpu'] = c.line_html(
                    'cpu使用率日志[1小时]',
                    attr_cpu,
                    vals_cpu,
                    'red'
                )
            else:
                data['line_mem'] = "<div class='alert alert-danger'>没有cpu使用率数据[1小时内]</div>"

            # 交换区折线图
            if attr_swap and vals_swap:
                data['line_swap'] = c.line_html(
                    '交换区使用率日志[1小时]',
                    attr_swap,
                    vals_swap,
                    'green'
                )
            else:
                data['line_swap'] = "<div class='alert alert-danger'>没有交换区使用率数据[1小时内]</div>"

            # 内存折线图
            if attr_mem and vals_mem:
                data['line_mem'] = c.line_html(
                    '内存使用率日志[1小时]',
                    attr_mem,
                    vals_mem,
                    'blue'
                )
            else:
                data['line_mem'] = "<div class='alert alert-danger'>没有内存使用率数据[1小时内]</div>"

        # 1天
        if int(id) == 2:
            attr_mem, vals_mem_min, vals_mem_max, vals_mem_avg, \
            attr_swap, vals_swap_min, vals_swap_max, vals_swap_avg, \
            attr_cpu, vals_cpu_min, vals_cpu_max, vals_cpu_avg = self.data_by_three()
            print(attr_mem, vals_mem_min, vals_mem_max, vals_mem_avg)

            # 内存
            if attr_mem and vals_mem_min and vals_mem_max and vals_mem_avg:
                data['line_mem'] = c.line_three_html(
                    '内存使用率日志[今天]',
                    attr_mem,
                    vals_mem_min,
                    vals_mem_max,
                    vals_mem_avg,
                )
            else:
                data['line_mem'] = "<div class='alert alert-danger'>没有内存使用率数据[今天]</div>"
            # 交换分区
            if attr_swap and vals_swap_min and vals_swap_max and vals_swap_avg:
                data['line_swap'] = c.line_three_html(
                    '交换分区使用率日志[今天]',
                    attr_swap,
                    vals_swap_min,
                    vals_swap_max,
                    vals_swap_avg,
                )
            else:
                data['line_swap'] = "<div class='alert alert-danger'>没有交换分区使用率数据[今天]</div>"
            # cpu
            if attr_cpu and vals_cpu_min and vals_cpu_max and vals_cpu_avg:
                data['line_cpu'] = c.line_three_html(
                    'cpu使用率日志[今天]',
                    attr_cpu,
                    vals_cpu_min,
                    vals_cpu_max,
                    vals_cpu_avg,
                )
            else:
                data['line_cpu'] = "<div class='alert alert-danger'>没有cpu使用率数据[今天]</div>"

        # id = 3表示1个月内
        if int(id) == 3:
            attr_mem, vals_mem_min, vals_mem_max, vals_mem_avg, \
            attr_swap, vals_swap_min, vals_swap_max, vals_swap_avg, \
            attr_cpu, vals_cpu_min, vals_cpu_max, vals_cpu_avg = self.data_by_three(
                method="month",
                format="%Y%m%d"
            )
            if attr_mem and vals_mem_min and vals_mem_max and vals_mem_avg:
                data['line_mem'] = c.line_three_html(
                    "内存使用率日志[本月]",
                    attr_mem,
                    vals_mem_min,
                    vals_mem_max,
                    vals_mem_avg
                )
            else:
                data["line_mem"] = "<div class='alert alert-danger'>没有内存[本月]数据</div>"
            if attr_swap and vals_swap_min and vals_swap_max and vals_swap_avg:
                data['line_swap'] = c.line_three_html(
                    "交换分区使用率日志[本月]",
                    attr_swap,
                    vals_swap_min,
                    vals_swap_max,
                    vals_swap_avg
                )
            else:
                data["line_swap"] = "<div class='alert alert-danger'>没有交换分区[本月]数据</div>"
            if attr_cpu and vals_cpu_min and vals_cpu_max and vals_cpu_avg:
                data['line_cpu'] = c.line_three_html(
                    "CPU使用率日志[本月]",
                    attr_cpu,
                    vals_cpu_min,
                    vals_cpu_max,
                    vals_cpu_avg
                )
            else:
                data["line_cpu"] = "<div class='alert alert-danger'>没有CPU[本月]数据</div>"

        self.render('log.html', data=data)

    def data_by_hour(self):
        """获取一小时内的数据"""
        now_time, next_time = self.date_range()
        attr_cpu, attr_swap, attr_mem = None, None, None  # 属性
        vals_cpu, vals_swap, vals_mem = None, None, None  # 值

        session = ORM.db()
        try:
            # cpu
            cpu = self.one_hour_query(model=Cpu, session=session, now_time=now_time, next_time=next_time)
            if cpu:
                attr_cpu = [v.create_time.strftime("%H:%M:%S") for v in cpu]
                vals_cpu = [float(v.percent) for v in cpu]

            # 交换区
            swap = self.one_hour_query(model=Swap, session=session, now_time=now_time, next_time=next_time)
            if swap:
                attr_swap = [v.create_time.strftime("%H:%M:%S") for v in swap]
                vals_swap = [float(v.percent) for v in swap]

            # 内存
            mem = self.one_hour_query(model=Mem, session=session, now_time=now_time, next_time=next_time)
            if mem:
                attr_mem = [v.create_time.strftime("%H:%M:%S") for v in mem]
                vals_mem = [float(v.percent) for v in mem]  # decimal不能转化为json，需要转换为float
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()

        return attr_cpu, attr_swap, attr_mem, vals_cpu, vals_swap, vals_mem

    def one_hour_query(self, model, session, now_time, next_time):
        """
        查询一小时内的model，范围为create_dt[now_time, next_time)
        """
        data = session.query(model).order_by(model.create_dt.asc()).filter(
            and_(
                model.create_dt >= now_time.strftime("%Y-%m-%d %H") + ":00:00",
                model.create_dt < next_time.strftime("%Y-%m-%d %H") + ":00:00"
            )
        ).all()
        return data

    def data_by_three(self, method='day', format="%Y%m%d%H"):
        """按照小时和天查询今天和本月最大最小值"""
        session = ORM.db()
        attr_mem, vals_mem_min, vals_mem_max, vals_mem_avg = None, None, None, None
        attr_swap, vals_swap_min, vals_swap_max, vals_swap_avg = None, None, None, None
        attr_cpu, vals_cpu_min, vals_cpu_max, vals_cpu_avg = None, None, None, None
        try:
            # 内存
            mem = self.three_query(Mem, session, method, format)
            if mem:
                attr_mem = [v[0] for v in mem]
                vals_mem_min = [float(v[1]) for v in mem]
                vals_mem_max = [float(v[2]) for v in mem]
                vals_mem_avg = [round(float(v[3]), 1) for v in mem]
            # 交换分区
            swap = self.three_query(Swap, session, method, format)
            if swap:
                attr_swap = [v[0] for v in swap]
                vals_swap_min = [float(v[1]) for v in swap]
                vals_swap_max = [float(v[2]) for v in swap]
                vals_swap_avg = [round(float(v[3]), 1) for v in swap]
            # CPU
            cpu = self.three_query(Cpu, session, method, format)
            if cpu:
                attr_cpu = [v[0] for v in cpu]
                vals_cpu_min = [float(v[1]) for v in cpu]
                vals_cpu_max = [float(v[2]) for v in cpu]
                vals_cpu_avg = [round(float(v[3]), 1) for v in cpu]
        except Exception as e:
            session.rollback()
        else:
            session.commit()
        finally:
            session.close()
        return attr_mem, vals_mem_min, vals_mem_max, vals_mem_avg, \
               attr_swap, vals_swap_min, vals_swap_max, vals_swap_avg, \
               attr_cpu, vals_cpu_min, vals_cpu_max, vals_cpu_avg

    def three_query(self, model, session, method="day", format="%Y%m%d%H"):
        """查询最大值、最小值、平均值"""
        model_query = session.query(
            func.date_format(model.create_dt, format),
            func.min(model.percent),
            func.max(model.percent),
            func.avg(model.percent)
        )
        data = None
        if method == "day":
            # 过滤出今天的数据
            # 按照小时分组
            # 按照时间升序排序
            data = model_query.filter(
                func.to_days(model.create_dt) == func.to_days(func.now())
            ).group_by(
                func.date_format(model.create_dt, format)
            ).order_by(model.create_dt.asc()).all()
        if method == "month":
            # 过滤出当前月的数据
            # 按照天来分组
            # 按照时间升序排序
            data = model_query.filter(
                func.date_format(model.create_dt, "%Y%m") == func.date_format(func.curdate(), "%Y%m")
            ).group_by(
                model.create_date
            ).order_by(model.create_dt.asc()).all()
        return data

    def date_range(self):
        """获取时间范围"""
        now_time = datetime.datetime.now()
        next_time = now_time + datetime.timedelta(hours=1)  # 下一小时
        return now_time, next_time

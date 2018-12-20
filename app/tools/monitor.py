#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/14
@file:monitor.py
@desc:
"""
import psutil
import time
import datetime
from pprint import pprint


class Monitor(object):
    """定义获取系统信息的类"""

    def cpu(self):
        """获取CPU信息"""

        # interval指定刷新周期，percpu指定是否统计每个cpu
        data = dict(
            percent_avg=psutil.cpu_percent(interval=0, percpu=False),  # 平均
            percent_per=psutil.cpu_percent(interval=0, percpu=True),  # 每个
            num_p=psutil.cpu_count(logical=False),  # 物理CPU核数
            num_l=psutil.cpu_count(logical=True),  # 逻辑CPU核数
        )

        return data

    def mem(self):
        """获取内存信息"""

        # 返回svmem(total=6351052800, available=1593049088, percent=74.9, used=4758003712, free=1593049088)
        info = psutil.virtual_memory()
        data = dict(
            total=self.bytes_to_gb(info.total),
            used=self.bytes_to_gb(info.used),
            free=self.bytes_to_gb(info.free),
            percent=info.percent,
        )
        return data

    def swap(self):
        """获取交换分区信息"""

        info = psutil.swap_memory()
        data = dict(
            total=self.bytes_to_gb(info.total),
            used=self.bytes_to_gb(info.used),
            free=self.bytes_to_gb(info.free),
            percent=info.percent,
        )
        return data

    def disk(self):
        """获取磁盘分区信息"""

        # [sdiskpart(device='C:\\', mountpoint='C:\\', fstype='NTFS', opts='rw,fixed'),
        #  sdiskpart(device='D:\\', mountpoint='D:\\', fstype='NTFS', opts='rw,fixed'),
        #  sdiskpart(device='E:\\', mountpoint='E:\\', fstype='NTFS', opts='rw,fixed')]
        info = psutil.disk_partitions()
        data = [
            dict(
                device=v.device,
                mountpoint=v.mountpoint,
                fstype=v.fstype,
                opts=v.opts,
                used={
                    k: self.bytes_to_gb(v, key=k)
                    for k, v in psutil.disk_usage(v.mountpoint)._asdict().items()
                }
            )
            for v in info
        ]
        return data

    def net(self):
        """获取网卡信息"""

        # 获取地址信息
        addrs = psutil.net_if_addrs()
        # val.family.name == 'AF_INET' 只保留IPV4的信息
        addrs_info = {
            k: [
                dict(
                    family=val.family.name,
                    address=val.address,
                    netmask=val.netmask,
                    broadcast=val.broadcast
                )
                for val in v if val.family.name.endswith("AF_INET")
            ]
            for k, v in addrs.items()
        }
        addrs_info_ = dict()
        for k, v in addrs_info.items():
            if len(v) > 0:
                addrs_info_.update({k: v[0]})
        # 获取输入输出信息
        io = psutil.net_io_counters(pernic=True)
        data = [
            dict(
                name=k,
                bytes_sent=v.bytes_sent,
                bytes_recv=v.bytes_recv,
                packets_sent=v.packets_sent,
                packets_recv=v.packets_recv,
                **addrs_info_.get(k)
            )
            for k, v in io.items() if addrs_info_.get(k)
        ]
        return data

    def get_last_boot(self):
        """获取最近开机时间"""
        return self.to_datetime(psutil.boot_time())

    def get_user(self):
        """获取登录用户信息"""
        users = psutil.users()
        users_info = [
            dict(
                name=u.name,
                terminal=u.terminal,
                host=u.host,
                started=self.to_datetime(u.started),
                pid=u.pid,
            )
            for u in users
        ]
        return users_info

    @staticmethod
    def to_datetime(tm):
        """时间戳转化成日期"""
        dt = datetime.datetime.fromtimestamp(tm)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def bytes_to_gb(value, key=''):
        """字节转GB"""
        if key == 'percent':
            return value
        else:
            return round(value / (1024 ** 3), 2)

    @staticmethod
    def dt():
        """获取当前时间"""
        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return dt


if __name__ == '__main__':
    m = Monitor()
    for _ in range(1):
        # pprint(m.cpu())
        # pprint(m.mem())
        # pprint(m.swap())
        # pprint(m.disk())
        pprint(m.net())
        # pprint(m.get_last_boot())
        # pprint(m.get_user())
        time.sleep(1)

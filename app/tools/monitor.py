#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/14
@file:monitor.py
@desc:
"""
import psutil
import time
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

    @staticmethod
    def bytes_to_gb(value, key):
        """字节转GB"""
        if key == 'percent':
            return value
        else:
            return round(value / (1024 ** 3), 2)


if __name__ == '__main__':
    m = Monitor()
    for _ in range(1):
        # pprint(m.cpu())
        # pprint(m.mem())
        # pprint(m.swap())
        pprint(m.disk())
        time.sleep(1)

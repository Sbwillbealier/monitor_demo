#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author:Created by GJ on 2018/12/16
@file:view_real_time.py
@desc:
'''
from sockjs.tornado import SockJSConnection


class RealTimeHandler(SockJSConnection):
    """websocket实时监控类"""

    # 定义一个连接池，管理所以连接客户端
    waiters = set()

    def on_open(self, request):
        """建立连接"""
        try:
            self.waiters.add(self)
        except Exception as e:
            print(e)

    def on_message(self, message):
        """接收消息"""
        try:
            # 接收消息并处理，把新消息发给所有客户端
            self.broadcast(self.waiters, message)  # 广播
        except Exception as e:
            print(e)

    def on_close(self):
        """关闭连接"""
        try:
            self.waiters.remove(self)
        except Exception as e:
            print(e)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/5
@file:__init__.py.py
@desc:
"""
import tornado.web  # web 框架
import tornado.httpserver  # http服务
import tornado.ioloop  # 输入/输出事件循环
import tornado.options  # 配置工具

from tornado.options import options, define  # 选项、定义配置
from app.configs import configs
from app.urls import urls

# 定义一个服务端口
define("port", default=8000, type=int, help='运行端口')


# 1.自定义应用
class Application(tornado.web.Application):
    """自定义应用类"""

    def __init__(self):
        # 路由规则
        headers = urls

        # 配置信息
        settings = configs

        super(Application, self).__init__(headers, **settings)


# 2.自定义服务器
def create_server():
    """创建自定义的服务器"""

    # 允许命令行启动
    tornado.options.parse_command_line()

    # 创建应用对象
    app = Application()

    # 创建http服务器，绑定端口
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    # 启动循环监听
    tornado.ioloop.IOLoop.current().start()

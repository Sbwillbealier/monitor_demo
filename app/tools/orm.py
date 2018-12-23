#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/21
@file:orm.py
@desc:
"""
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class ORM(object):
    """orm模型"""

    @staticmethod
    def db():
        """返回数据库操作会话"""
        # 配置连接信息
        mysql_configs = dict(
            host="127.0.0.1",
            port=3306,
            user="root",
            pwd="root",
            name="monitor"
        )

        link = "mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{name}".format(
            **mysql_configs
        )

        # 创建连接引擎, 指定编码utf-8， 输出日志echo
        engine = create_engine(
            link,
            encoding='utf-8',
            echo=False,  # 显示错误信息
            pool_size=100,  # 连接池大小
            pool_recycle=10,
            connect_args={"charset": "utf8"}
        )

        # 创建session
        Session = sessionmaker(
            bind=engine,
            autocommit=False,
            autoflush=True,
            expire_on_commit=False,
        )
        return Session()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author:Created by GJ on 2018/12/13
@file:models.py
@desc:
    1. 导入模型继承父类
    2.导入数据类型
    3.导入闯进字段的类
    4.定义模型
"""
from sqlalchemy.ext.declarative import declarative_base  # 模型继承父类
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL, DATE, TIME, DATETIME  # 导入数据类型
from sqlalchemy import Column  # 导入字段类

Base = declarative_base()  # 创建对象的基类
metadata = Base.metadata  # 创建元类


# 定义内存模型
class Mem(Base):
    __tablename__ = 'mem'  # 指定表名
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    total = Column(DECIMAL(8, 2))
    used = Column(DECIMAL(8, 2))
    free = Column(DECIMAL(8, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


# 定义交换分区模型
class Swap(Base):
    __tablename__ = 'swap'  # 指定表名
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    total = Column(DECIMAL(8, 2))
    used = Column(DECIMAL(8, 2))
    free = Column(DECIMAL(8, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


# 定义CPU模型
class Cpu(Base):
    __tablename__ = 'cpu'
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


if __name__ == '__main__':
    # 1.导入数据库连接驱动
    import mysql.connector

    # 2.导入创建引擎
    from sqlalchemy import create_engine

    # 配置连接信息
    mysql_configs = dict(
        host="127.0.0.1",
        port=3306,
        user="root",
        pwd="root",
        name="monitor"
    )

    # 连接格式： mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
    # 连接格式： mysql+驱动名称://用户名:密码@主机:端口/数据库名称
    link = "mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{name}".format(
        **mysql_configs
    )


    # 创建连接引擎, 指定编码utf-8， 输出日志echo
    engine = create_engine(link, encoding='utf-8', echo=True)

    # 映射到数据库
    metadata.create_all(engine)

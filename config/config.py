# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  config.py
@Description    :  
@CreateTime     :  2022/2/14 12:02
------------------------------------
@ModifyTime     :  
"""
import os
import secrets
from typing import List

from pydantic import AnyHttpUrl, BaseSettings


class Settings(BaseSettings):
    """
    项目基础设置
    """
    APP_NAME = "Auto Test Manage System"  # api文档名称
    # 接口文档设置
    TITLE: str = 'Auto Test Manage System'
    DESC: str = """
        `主要解决项目管理、团队管理、数据Mock、信息化同步、工时管理等研发问题`
        - 前端：`Vue2`  `ElementUI`   
        - 后端: `Python` ` FastAPI ` `Tortoise ORM`  `MySQL`

        **资料汇总**
        - [x] [Github源码]()

        """

    API_PREFIX = "/v1"  # api访问前缀

    # Token 相关
    ALGORITHM: str = "HS256"  # 加密算法
    # jwt密钥, 建议随机生成一个
    SECRET_KEY: str = secrets.token_urlsafe(32)  # 随机生成base64位字符串
    # token过期时间
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # token时效 30 天 = 60 * 24 * 30

    # 跨域设置
    ORIGINS: List[str] = ["*"]
    # 跨域白名单
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost:3000"]

    # 数据库配置
    DB_URL = "mysql://root:123456@localhost:3306/atms"  # 本地开发数据库

    # 项目环境配置
    ENV = os.environ.get("fast_env", "DEV")  # 本次启动环境
    PORT = 8999  # 启动端口配置
    RELOAD = True  # 是否热加载
    DEBUG = False  # 是否开启调试模式


settings = Settings()

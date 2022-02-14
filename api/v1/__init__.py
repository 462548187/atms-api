# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  __init__.py
@Description    :  
@CreateTime     :  2022/2/14 12:40
------------------------------------
@ModifyTime     :  
"""
from fastapi import APIRouter
from .login import login_router

v1 = APIRouter(prefix="/v1")

# v1.include_router(login_router)

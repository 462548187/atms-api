# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  view.py
@Description    :  
@CreateTime     :  2022/2/14 15:39
------------------------------------
@ModifyTime     :  
"""
from fastapi import APIRouter

login_router = APIRouter(tags=["登录相关"])


@login_router.post("/login", name="登录")
async def login():
    pass


@login_router.post("/logout", name="登出")
async def logout():
    pass

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
import datetime
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

import core
from models import user
from config import settings
from utils import security

login_router = APIRouter(tags=["登录相关"])


@login_router.post("/login", name="登录")
async def login(request: Request, user_form: OAuth2PasswordRequestForm = Depends()):
    """
    登录接口
    """
    # 1.用户信息获取
    username = user_form.username
    password = user_form.password

    # 2.数据库校验
    is_exist_user = await user.User.filter(username=username, is_delete=0)
    user_obj = await user.User.get(username=username)
    print(is_exist_user)

    if len(is_exist_user) > 0:
        # 停用的不让登录
        if user_obj.status == 2:
            content = {"code": 500, "msg": "该用户已停用,请联系管理员!"}
            return JSONResponse(content=content)

        # 判断用户是否激活
        if user_obj.is_active == 0:
            # logger.error(f"{user_name.username}未激活")
            content = {"code": 500, "msg": "该用未激活,请联系管理员!"}
            return JSONResponse(content=content)

        # print(security.get_password_hash(password))
        if not security.verify_password(password, user_obj.password):
            content = {"code": 500, "msg": "用户名或密码错误"}
            return JSONResponse(content=content)

        # 启用的正常执行
        # 3.token生成
        expire_time = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token({"sub": user_obj.username}, expire_time)

        # 4.返回token及用户信息
        # 日期格式需要转成字符串

        login_date = datetime.datetime.now()
        ip = request.client.host
        await user.User.filter(username=username).update(ip=ip, last_login_date=login_date)
        content = {"code": 200, "msg": "登录成功", "token_type": "bearer", "access_token": access_token, "user": username}
        return JSONResponse(content=content)
    else:
        content = {"code": 500, "msg": "用户不存在!!!"}
        return JSONResponse(content=content)


@login_router.post("/logout", name="登出")
async def logout(token: str = Depends(security.get_current_user)):
    return core.Success(data=token)

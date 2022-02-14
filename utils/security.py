# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
------------------------------------
@File           :  security.py
@Description    :
@CreateTime     :  2022/2/14, 19:44
------------------------------------
@ModifyTime     :
"""
from datetime import timedelta, datetime
from typing import Optional

# token 路由
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
# jwt库
from jose import jwt, JWTError

# hash 密码库
from passlib.context import CryptContext

from config import settings

# 密码加密算法
from models import user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 生成token 的指定路由
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/login")


def get_password_hash(password: str) -> str:
    """使用哈希算法加密密码"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码与hash密码"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expire_time: Optional[timedelta] = None):
    """
    生成JWT token
    """

    # 设置token过期时间
    if expire_time:
        expire = datetime.utcnow() + expire_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    获取当前登陆用户
    """
    token_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token不正确或已过期",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        jwt_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = jwt_data.get("sub")
        if username is None or username == "":
            raise token_exception
    except JWTError:
        raise token_exception
    user_name = await user.User.get(username=username)
    if user_name is None:
        raise token_exception
    return user_name

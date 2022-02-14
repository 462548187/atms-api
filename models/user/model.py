# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :  
------------------------------------
@File           :  model.py
@Description    :  
@CreateTime     :  2022/2/14 14:24
------------------------------------
@ModifyTime     :  
"""
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model


class User(Model):
    id = fields.IntField(pk=True, index=True, description="ID")
    username = fields.CharField(max_length=32, description="登录名称", unique=True)
    password = fields.CharField(max_length=255, description="用户密码")
    name = fields.CharField(max_length=25, description="姓名")
    email = fields.CharField(max_length=50, description="邮箱", null=True)
    mobile = fields.CharField(max_length=11, description="手机", null=True)
    department = fields.CharField(max_length=20, description="部门", null=True)
    avatar = fields.CharField(max_length=255, default="/static/default.jpg", description="头像")
    ip = fields.CharField(max_length=255, description="登录ip")
    # 状态,1表示启用，0表示停用
    is_active = fields.BooleanField(default='1', description="是否激活")
    # 软删除，0表示未删除，1表示删除
    is_delete = fields.BooleanField(description="是否已删除", default='0')
    # 状态,1表示启用，2表示停用
    status = fields.IntField(description="是否在职", default='1')
    last_login_date = fields.DatetimeField(auto_now=True, description="最后登录时间")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    modified_time = fields.DatetimeField(auto_now=True, description="修改时间")

    # 查询集最大递归层级
    class PydanticMeta:
        max_recursion = 1


# 返回模型
User_Pydantic = pydantic_model_creator(User, name="User", exclude=("password",))

# 输入模型 exclude_readonly 只读字段 非必填
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude=("avatar",), exclude_readonly=True)

# # !/usr/bin/python3
# # -*- coding: utf-8 -*-
# """
# @Author         :  Liu Yue
# @Version        :
# ------------------------------------
# @File           :  models.py
# @Description    :
# @CreateTime     :  2022/2/14 12:39
# ------------------------------------
# @ModifyTime     :
# """
# from tortoise import fields, Tortoise
# from tortoise.contrib.pydantic import pydantic_model_creator
# from tortoise.models import Model
#
#
# # 公共抽象模型
# class AbstractModel(Model):
#     id = fields.IntField(pk=True, index=True, description="ID")
#     # 软删除，0表示未删除，1表示删除
#     is_delete = fields.BooleanField(description="是否已删除", default='0')
#     create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
#     modified_time = fields.DatetimeField(auto_now=True, description="修改时间")
#
#
# class User(AbstractModel):
#     username = fields.CharField(max_length=32, description="登录名称")
#     password = fields.CharField(max_length=255, description="用户密码")
#     name = fields.CharField(max_length=25, description="员工姓名")
#     email = fields.CharField(max_length=50, description="邮箱", null=True)
#     mobile = fields.CharField(max_length=11, description="手机", null=True)
#     department = fields.CharField(max_length=20, description="部门", null=True)
#     avatar = fields.CharField(max_length=255, default="/static/default.jpg", description="用户头像")
#     ip = fields.CharField(max_length=255, description="登录ip")
#     # 状态,1表示启用，0表示停用
#     is_active = fields.BooleanField(default='1', description="是否激活登录账号")
#     # 状态,1表示启用，2表示停用
#     status = fields.IntField(description="是否在职", default='1')
#     last_login_date = fields.DatetimeField(auto_now=True, description="最后登录时间")
#
#     # 查询集最大递归层级
#     class PydanticMeta:
#         max_recursion = 1
#
#
# class Project(AbstractModel):
#     name = fields.CharField(max_length=20, description="项目名称")
#     desc = fields.TextField(description="项目描述", null=True)
#     status = fields.IntField(description="项目状态", default='1')
#
#     # 查询集最大递归层级
#     class PydanticMeta:
#         max_recursion = 1
#
#
# class Story(AbstractModel):
#     name = fields.CharField(max_length=20, description="需求名称")
#     project = fields.ForeignKeyField('models.Project', related_name='story_router', description="项目ID")
#     type = fields.CharEnumField(StoryType, default=StoryType.Demand,
#                                 description="需求类型:Demand = '需求',Optimization = '优化',Bug = '缺陷',Other = '其他'")
#     desc = fields.TextField(description="需求描述", null=True)
#     story_path = fields.CharField(max_length=255, description="需求链接", null=True, default="")
#     story_priority = fields.CharEnumField(PriorityType, default=PriorityType.Default,
#                                           description="优先级:Urgent = '紧急', High = '高' ,Middle = '中',Low = '低',"
#                                                       "insignificant = '无关紧要', Default = '空'")
#     status = fields.CharEnumField(ReceiveStatus, default=ReceiveStatus.Not_Started,
#                                   description="任务状态:Not_Started = '未开始', In_Progress = '进行中', Pause = '暂停', "
#                                               "Finished = '完成',Cancel = '取消'")
#     review_time = fields.CharField(max_length=32, description="评审时间", null=True)
#     confirm_time = fields.CharField(max_length=32, description="交底时间", null=True)
#     deleted = fields.IntField(description="是否已删除", default='0')
#     remark = fields.TextField(description="备注", null=True)
#
#     class PydanticMeta:
#         max_recursion = 2
#
#
# class Task(AbstractModel):
#     name = fields.CharField(max_length=20, description="任务名称")
#     story = fields.ForeignKeyField('models.Story', related_name='task', description="需求ID")
#     task_priority = fields.CharEnumField(PriorityType, default=PriorityType.Default,
#                                          description="优先级:Urgent = '紧急', High = '高' ,Middle = '中',Low = '低',"
#                                                      "insignificant = '无关紧要', Default = '空'")
#     story_name = fields.ManyToManyField('models.Staff', related_name='task', through='task_story', description="产品员工ID")
#     dev_name = fields.ManyToManyField('models.Staff', related_name='task1', through='task_dev', description="开发员工ID")
#     tester_name = fields.ManyToManyField('models.Staff', related_name='task2', through='task_tester',
#                                          description="测试员工ID")
#     test_time = fields.CharField(max_length=32, description="提测时间", null=True)
#     online_time = fields.CharField(max_length=32, description="上线时间", null=True)
#     server = fields.CharField(max_length=255, description="发布服务", null=True)
#     status = fields.CharEnumField(ReceiveStatus, default=ReceiveStatus.Not_Started,
#                                   description="任务状态:Not_Started = '未开始', In_Progress = '进行中', Pause = "
#                                               "'暂停', Finished = '完成',Cancel = '取消'")
#     delay = fields.IntField(description="是否延期", null=True)
#     deleted = fields.IntField(description="是否已删除", default='0')
#     remark = fields.TextField(description="备注", null=True)
#
#     class PydanticMeta:
#         max_recursion = 2
#
#
# class Push(AbstractModel):
#     name = fields.CharField(max_length=20, description="推送名称")
#     project = fields.ForeignKeyField('models.Project', related_name='push', description="项目ID")
#     receive = fields.CharEnumField(ReceiveType, default=ReceiveType.Dingding,
#                                    description="接收方式:Dingding = '钉钉', Email = '邮件', Wechat = '微信'")
#     at_name = fields.ManyToManyField(model_name='models.Staff', related_name='push', through='push_staff',
#                                      description="通知自定义ID")
#     access_token = fields.CharField(max_length=255, description="webhook", null=True)
#     secret = fields.CharField(max_length=255, description="secret", null=True)
#     at_all = fields.IntField(description="通知所有人", default='0')
#     is_active = fields.IntField(description="是否激活", default='1')
#     deleted = fields.IntField(description="是否已删除", default='0')
#
#     class PydanticMeta:
#         max_recursion = 2
#
#
# class DbSetting(AbstractModel):
#     id = fields.IntField(pk=True)
#     connect_name = fields.CharField(max_length=32, description='连接名称')
#     host = fields.CharField(max_length=32)
#     port = fields.IntField(description='端口')
#     user = fields.CharField(max_length=32)
#     password = fields.CharField(max_length=32)
#     db_name = fields.CharField(max_length=512)
#     env = fields.CharField(max_length=32, description='环境')
#     app = fields.CharField(max_length=32, description='应用名称')
#
#     class PydanticMeta:
#         max_recursion = 2
#
#
# # 解决pydantic_model_creator 生成的模型中 缺少外键关联字段
# Tortoise.init_models(["db.models"], "models")
#
# # 数据库配置相关
# DbSetting_Pydantic = pydantic_model_creator(DbSetting, name="DbSetting")
# DbSettingIn_Pydantic = pydantic_model_creator(DbSetting, name="DbSettingIn", exclude_readonly=True)
#
# # 返回模型
# User_Pydantic = pydantic_model_creator(Staff, name="Staff", exclude=("password",))
#
# # 输入模型 exclude_readonly 只读字段 非必填
# UserIn_Pydantic = pydantic_model_creator(Staff, name="StaffIn", exclude=("avatar",), exclude_readonly=True)
#
# # 员工相关
# Staff_Pydantic = pydantic_model_creator(Staff, name="Staff")
# StaffIn_Pydantic = pydantic_model_creator(Staff, name="StaffIn", exclude_readonly=True)
#
# # 项目相关
# Project_Pydantic = pydantic_model_creator(Project, name="Project")
# ProjectIn_Pydantic = pydantic_model_creator(Project, name="ProjectIn", exclude_readonly=True)
#
# # 需求相关
# Story_Pydantic = pydantic_model_creator(Story, name="Story")
# StoryIn_Pydantic = pydantic_model_creator(Story, name="StoryIn", exclude_readonly=True)
#
# # 任务相关
# Task_Pydantic = pydantic_model_creator(Task, name="Task")
# TaskIn_Pydantic = pydantic_model_creator(Task, name="TaskIn", exclude_readonly=True)
#
# # 推送相关
# Push_Pydantic = pydantic_model_creator(Push, name="Push")
# PushIn_Pydantic = pydantic_model_creator(Push, name="PushIn", exclude_readonly=True)

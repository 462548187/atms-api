# !/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author         :  Liu Yue
@Version        :
@License        :   (C) Copyright 2021
------------------------------------
@File           :  manage.py
@Description    :  
@CreateTime     :  2021-08-04 14:45
------------------------------------
@ModifyTime     :
"""
import os
import sys
import argparse


def runserver():
    parser = argparse.ArgumentParser()
    parser.add_argument('runserver', nargs=1)
    parser.add_argument('--host', help='Bind socket to this host.  [default:0.0.0.0].')
    parser.add_argument('-p', '--port', help='Bind socket to this port.  [default: 8999].')
    parser.add_argument('--reload', nargs='?', default=True, help='Enable auto-reload.')  # 有填写则为None

    # 获取参数
    args = parser.parse_args()
    host = args.host
    port = args.port
    reload = args.reload

    # 拼接
    command = 'uvicorn main:app'
    if host:
        command += f' --host={host}'
    if port:
        command += f' --port={port}'
    if reload is None:
        command += f' --reload'

    # 执行命令
    os.system(command)
    # try:
    #     subprocess.run(command, shell=True)
    # except KeyboardInterrupt:
    #     time.sleep(0.5)
    #     print('exit.')


def help_info():
    print('\033[32m帮助信息：')
    print('\033[0m\trunserver           运行服务 --host [ip]服务器地址 '
          ' -p --post [int]端口号 -w -workers [int]进程数 --reload 是否自动加载')


def main():
    if len(sys.argv) < 2:
        command = 'help'
    else:
        command = sys.argv[1]

    if command == 'startproject':
        if len(sys.argv) < 3:
            print('error: You must provide a project name.')
            sys.exit()

    elif command == 'runserver':
        runserver()

    elif command == 'help':
        help_info()

    else:
        print('\033[31mError:错误的命令')
        help_info()


if __name__ == '__main__':
    main()

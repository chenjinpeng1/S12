#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"

"""
the cmd execution module
mysalt "operate object" module.func "instruction"
arg = ["operate object", module.func, "instruction"]
"""
import paramiko
import os
import sys
import logging
from multiprocessing import Pool
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core import handler
loger = logging.getLogger(__name__)


# 执行命令
def cmd_func(ip, cmd):
	# 创建SSH对象
	ssh = paramiko.SSHClient()
	# 允许连接不在know_hosts文件中的主机
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	# 连接服务器
	ssh.connect(hostname=i, port=22, username="root", password="rootroot")
	# 执行命令
	stdin, stdout, stderr = ssh.exec_command(cmd)
	result = stdout.read() if stdout.read() else stderr.read()
	ssh.close()
	print("IP:{} return==>:".format(ip))
	print(result.decode())


def run(arg):
	pool = Pool(5)
	print("Execute the command in batch.")
	if len(arg) != 2:
		loger.info("Lack of arguments.acquired arg:{}".format(arg))
	else:
		obj_list, cmd_list = arg
		ip_list = handler.myhandler(obj_list)
		cmd = " ".join(cmd_list)
		for i in ip_list:
			pool.apply_async(cmd_func, args=(i, cmd))
		pool.close()
		pool.join()

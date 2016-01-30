#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"

import random

print(random.random())
# 包含边界
print(random.randint(1, 3))
# 不包含边界
print(random.randrange(1, 3))

# 生成4位随机验证码
check_code = ""
for i in range(4):
	current = random.randrange(0, 4)
	if current != i:
		temp = chr(random.randint(97, 122))
	else:
		temp = random.randint(0, 9)
	check_code = "{}{}".format(check_code, temp)

print(check_code)

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"

"""
购物商城
"""

import os
import re
import sys
from collections import OrderedDict
from collections import Counter

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

from general_module import db_operater
from general_module import db_operater
from general_module import md5_encryption
from mall_login import mall_login

shop_dic = {"MacBook Air": 7999, "Starbucks Coffee": 33, "iphone 6 Plus": 6188, "Air Jordan S.F 4": 888, "Casio": 1799}
shopping_cart_list = []


# 初始化商品目录
def init_shop_dic(dic):
	print("This is Q1mi's shopping mall,below are the things we are selling:")
	return OrderedDict(sorted(dic.items(), key=lambda t: t[1]))   # 价格从低到高排序成有序字典


# 打印商品列表
def print_shop_dic(dic):
	for i, key in enumerate(dic, 1):
		print("%s. %-20s%10s" % (i, key, dic[key]))   # 打印出序号与物品名称及价格


# 生成一个选项与物品名称及价格对应的字典
def get_price_dict(dic):
	index_list = []
	content_list = []
	for i in range(1, len(dic) + 1):
		index_list.append(i)
	for j in dic.items():
		content_list.append(j)
	return dict(list(zip(index_list, content_list)))  # 字典格式：选项：(物品名称：价格)


# 获取总价
# def get_prices(cart_list, ord_dic):
# 	print("正在结算，请稍后...")
# 	print("购物清单：".center(75))
# 	shopping_cart_count = Counter(cart_list)   # Counter统计序列中元素出现的次数
# 	total_prices = 0
# 	for key, val in shopping_cart_count.items():    # 打印出用户的购物清单
# 		print("商品名称：%-20s 数量：%-10s 单价：%8s 总价：%8s" % (
# 			key, shopping_cart_count[key], ord_dic[key], ord_dic[key] * shopping_cart_count[key]))
# 		total_prices += ord_dic[key] * shopping_cart_count[key]
# 	return total_prices


# 信用卡支付接口
def check_out(arg):
	db_file_tmp = "{}/database/card_account.db".format(os.path.dirname(os.path.dirname(__file__)))
	db_file = os.path.abspath(db_file_tmp)
	info = db_operater.read_db(db_file)
	while True:
		card_id = input("请输入信用卡卡号（8位数字）：")
		if re.match(r'^\d{8}$', card_id):
			if info.get(card_id, None):
				card_passwd = input("请输入密码：")
				if md5_encryption.md5_encryption(card_passwd) == info[card_id].get("password", None):
					if info[card_id]["current_limit"] - arg >= 0:
						info[card_id]["current_limit"] -= arg
						print("结算完成！")
						db_operater.write_db(file=db_file, data=info)
						break
					else:
						print("余额不足！")
						break
				else:
					print("密码错误，请重新输入！")
			else:
				print("无效的卡号！请重新输入！")
		else:
			print("无效的卡号！请重新输入！")


# 打印购物车
def print_shopping_cart(dic):
	shopping_cart_count = Counter(shopping_cart_list)
	total_prices = 0
	for key, val in shopping_cart_count.items():
		print("商品名称：%-20s 数量：%-10s 单价：%8s 总价：%8s" % (
			key, shopping_cart_count[key], dic[key], dic[key] * shopping_cart_count[key]))
		total_prices += dic[key] * shopping_cart_count[key]
	print("-" * 75)
	return total_prices


# 判断选择
def get_user_input(level):
	while True:
		if level == 1:  # 当调用处于购物商城界面时，有以下菜单
			user_choose = input("请输入您的选择，按P查看购物车，按C结算，按Q退出：").strip()
			if user_choose.isdigit():
				user_choose = int(user_choose)
				return user_choose
			elif user_choose.upper() == 'C':
				return 'C'
			elif user_choose.upper() == 'P':
				return 'P'
			elif user_choose.upper() == 'Q':
				return 'Q'
			else:
				print("无效的输入，请重新输入！")
		elif level == 2:    # 当调用处于购物车界面时，有以下菜单
			user_choose = input("请输入您的选择，按B返回购物商城，按C结算， 按Q退出：").strip()
			if user_choose.upper() == 'B':
				return 'B'
			elif user_choose.upper() == 'Q':
				return 'Q'
			elif user_choose.upper() == 'C':
				return 'C'
			else:
				print("无效的输入，请重新输入！")
		else:   # 打印调用时的异常
			print("调用时出现参数错误！")


# 主函数
@mall_login
def main():
	checkout_flag = False   # 定义一个判断用户是否在购物车界面跳出的flag
	ordered_shop_dic = init_shop_dic(shop_dic)
	print_shop_dic(ordered_shop_dic)
	price_dict = get_price_dict(ordered_shop_dic)
	while not checkout_flag:
		option = get_user_input(1)
		if option == 'P':
			print("正在打印购物车...")
			print("我的购物车".center(71, '*'))
			print_shopping_cart(ordered_shop_dic)
			while True:
				option2 = get_user_input(2)    # 获取用户在购物车界面的输入
				if option2 == 'B':  # 用户输入B则返回购物商城界面
					print_shop_dic(ordered_shop_dic)
					break
				elif option2 == 'C':    # 用户在购物车界面输入C则结算
					print("此处调用结算功能。。。")
					print("购物清单：".center(75))
					a = print_shopping_cart(ordered_shop_dic)
					print("您此次消费总金额是：{}元".format(a))
					check_out(a)
					checkout_flag = True    # 用户在购物车界面结算时跳出主循环
					break   # 跳出购物车界面的循环
				elif option2 == 'Q':
					print("Bye~")
					checkout_flag = True
					break
				else:
					print("无效的输入，请重新输入！")
		elif option == 'C':    # 如果用户输入Q直接结算退出
			print("此处调用结算功能。。。")
			print("购物清单：".center(75))
			a = print_shopping_cart(ordered_shop_dic)
			print("您此次消费总金额是：{}元".format(a))
			check_out(a)
			break
		elif option == 'Q':
			print("Bye~")
			break
		else:
			if 0 < option <= len(ordered_shop_dic):   # 判断输入是否为有效数字
				object_name = price_dict[option][0]   # 定义物品名称
				shopping_cart_list.append(object_name)  # 将用户选择的物品名称加入购物车列表
				print("%s已加入购物车，按P查看购物车，按C结算， 按Q退出：" % price_dict[option][0])
			else:
				print("无效的输入，请重新输入！")


if __name__ == '__main__':
	main()

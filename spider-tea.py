# -*- coding = utf8 -*-
# @Time  :2022/1/18 16:47
# @Author : Nico
# File : spider-tea.py
# @Software: PyCharm


import requests     # 数据请求模块
import pprint       # 格式化输入模块
import csv          # 保存csv文件
import re           # 正则表达式，进行文字匹配
import sqlite3
import time

f = open('tea123.csv', mode='a', encoding='utf_8_sig', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
        '店铺名称',
        '店铺详情',
        '店铺评分',
        '评价人数',
        '人均消费',
        '店铺地址',
])
csv_writer.writeheader()        # 写入表头

# # 店铺名称
# findTitle = re.compile(r'<span class="title">(.*)</span>')
# # 店铺详情
# findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串的模式）
# # 店铺评分
# findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# # 评价人数
# findJuge = re.compile(r'<span>(\d*)人评价</span>')

for page in range(0, 1024, 32):
    # 发送请求，对于店铺数据包发送请求
    url = "https://apimobile.meituan.com/group/v4/poi/pcsearch/10"
    time.sleep(5)
    data = {
        'uuid': '8817595482324b0eb91e.1642555990.1.0.0',
        'userid': '2226566483',
        'limit': '32',
        'offset': page,
        'cateId': '-1',
        'q': '茶馆',
        'token': 'HK3U5iCemdttKbqiEz8uwayyOPYAAAAA9A8AALLZZzfKSoP_Q58PT80q3NTksAgzNFhrNdJg15pePs4nSBk7on5dRcBxx-49dybCQA',
    }

    headers= {
        'Referer': 'https://sh.meituan.com/',       # 防盗链，告诉服务器发送请求的url地址是从哪里跳转过来的
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }

    response = requests.get(url=url, params=data, headers=headers)
    # print(response.json())      # 获取json字典数据
    # pprint.pprint(response.json())
    # print(response)
    searchResult = response.json()['data']['searchResult']      # 键值对提取数据
    # print(searchResult)
    for items in searchResult:      # 遍历列表，逐一提取元素
        # pprint.pprint(items)
        shop_id = items['id']
        shop_url = f'https://www.meituan.com/meishi/{shop_id}/'
        data = {
            '店铺名称': items['title'],
            '店铺详情': shop_url,
            '店铺评分': items['avgscore'],
            '评价人数': items['comments'],
            '人均消费': items['avgprice'],
            '店铺地址': items['areaname'],

        }
        # csv_writer.writerow(data)       # 保存数据
        print(data)
f.close()
print("爬取完毕！")


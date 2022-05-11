# -*- coding = utf8 -*-
# @Time  :2022/1/20 22:57
# @Author : Nico
# File : recommend-milk.py
# @Software: PyCharm


import pandas as pd
from numpy import *

tea = pd.io.parsers.read_csv('D:/TeaDataAnalysis/milk.csv')
tea.head()

tea1 = tea.loc[:, ['店铺名称', '店铺详情', '评价人数', '店铺评分']]
tea1.head()

C = tea1['店铺评分'].mean()  # 所有店铺评分的均值
print("奶茶店铺评分均值：%f分" % C)

M = tea1['评价人数'].quantile(0.9)  # 筛选的评价顾客人数阈值，也就是如果某个店铺评价的个数低于阈值，则该店铺将被忽略不计
print("奶茶店铺评价人数阈值：%d" % M)  # M的取值可以根据需求自由选取，在下面的模型中，采用90分位值，也就是只选取评价人数为前10%的店铺进行分析

q_tea1 = tea1.copy().loc[tea1['评价人数'] > M]
q_tea1.shape


def weighted_rating(x, M=M, C=C):
    V = x['评价人数']  # 某店铺参与评价的顾客人数
    R = x['店铺评分']  # 该店铺的评分
    return round((V / (V + M) * R) + (M / (V + M) * C), 2)


"""
R 单个店铺的评分
V 单个店铺的有效评价人数
M 进入推荐前10%所需最低的有效评价人数
C 所有店铺的平均分
"""

q_tea1['综合得分'] = q_tea1.apply(weighted_rating, axis=1)

q_tea1 = q_tea1.sort_values('综合得分', ascending=False)
df = q_tea1.head(10)
list = []
for i in range(10):
    list.append(i + 1)
# print (list)
df.insert(0, 'id', list)
# df.to_csv('recommend-tea.csv', encoding='utf-8', index=False)
print(df)

# path = r'D:\TeaDataAnalysis\milk.db'
# conn = sql.connect(path)
# cursor = conn.cursor()
# from sqlalchemy import create_engine
# engine = create_engine(r'sqlite:///D:\TeaDataAnalysis\milk.db')
# df.to_sql('remilk', engine, if_exists='replace', index=False)


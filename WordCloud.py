# -*- coding = utf8 -*-
# @Time  :2022/1/7 9:39
# @Author : Nico
# File : WordCloud.py
# @Software: PyCharm

import jieba  # 分词，词云显示中文
from matplotlib import pyplot as plt  # 绘图，数据可视化
from wordcloud import WordCloud, STOPWORDS  # 词云
from PIL import Image  # 图像处理
import numpy as np  # 矩阵运算
import sqlite3  # 数据库
import pymysql
import pandas as pd

# 准备词云所需要的文字（词）
con = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='movie_demo')
cur = con.cursor()
sql = 'select 店铺名称 from milk'
# data = cur.execute(sql)
df = pd.read_sql('select 店铺名称 from milk', con)
text = ""
df['店铺名称'] = df['店铺名称'].str.split("（").str[0]
print(df['店铺名称'].tolist())
# for item in range(len(data)):
#     text = text + item[0]
#     # print(item[0])
# # print(text)
# cur.close()
# con.close()
#
# cut = jieba.cut(text)
string = ' '.join(df['店铺名称'].tolist())
# print(len(string))

stopwords = STOPWORDS
stopwords.add('茶馆')
stopwords.add('棋牌')
# stopwords.add('我')
# stopwords.add('人')
# stopwords.add('都')
# stopwords.add('了')
# stopwords.add('是')

img = Image.open(r'.\static\assets\img\tea.jpg')  # 打开遮罩图片
img_array = np.array(img)  # 将图片转换为数组
wc = WordCloud(
    # stopwords=stopwords,
    background_color='white',
    mask=img_array, font_path="msyh.ttc"  # 字体所在位置：C:\Windows\Fonts
)
wc.generate_from_text(string)

# 绘制图片
fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')  # 是否显示坐标轴

plt.show()  # 显示生成的词云图片

# 输出词云图片到文件
# plt.savefig(r'.\static\assets\img\3.jpg', dpi=500)


'''
@Project ：豆瓣250数据分析 
@File    ：cloud.py
@IDE     ：PyCharm 
@Author  ：一念之间
@Date    ：2022/5/31 18:54 
'''
import jieba                                #分词
from matplotlib import pyplot as plt       #绘图可视化
from PIL import Image                       #图片处理
import numpy as np                          #矩阵运算
import sqlite3
from wordcloud import WordCloud
conn=sqlite3.connect('movie.db')
cur=conn.cursor()
sql='select introduction from movie250'
data=cur.execute(sql)
text=""
for item in data:
    text=text+item[0]
# print(text)
cur.close()
conn.close()

cut=jieba.cut(text)
string=' '.join(cut)
print(len(string))
Img = Image.open(r'static/tree.png')  # 打开遮罩图片
img_arry = np.array(Img)  # 将图片转为数组
wc = WordCloud(
    background_color='white',
    mask=img_arry,
    font_path="simsun.ttc"   #字体位置在c:\windows\fonts
)
wc.generate_from_text(string)
#绘制图片
flg = plt.figure(1)
plt.imshow(wc)
plt.axis('off')
# plt.show()
plt.savefig(r'.\static\tree.jpg',dpi=200)
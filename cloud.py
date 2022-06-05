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
def wc(name,font):
    Img = Image.open(f'static/{name}.png')  # 打开遮罩图片
    img_arry = np.array(Img)  # 将图片转为数组
    wc = WordCloud(
        background_color='white',
        mask=img_arry,
        font_path=f"{font}"   #字体位置在c:\windows\fonts
    )
    wc.generate_from_text(string)
    #绘制图片
    flg = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    # plt.show()
    plt.savefig(f'./static/{name}.jpg',dpi=200)

def main():
    name="tree"
    name1="flower"
    name2="m"
    font="msyh.ttc"
    font1="simkai.ttf"
    font2="方正粗黑宋简体.ttf"
    wc(name,font)
    wc(name1,font1)
    wc(name2,font2)

if __name__ == '__main__':
    main()
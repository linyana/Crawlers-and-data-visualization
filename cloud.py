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
string=' '.join(cut).replace("的","").replace("是","").replace("你","").replace("我","").replace("们","").replace("不","").replace("了","").replace("人","").replace("就","").replace("都","").replace("电影","")
# print(len(string))
def wc(name,font):
    Img = Image.open(f'./static/img/{name}.png')  # 打开遮罩图片
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
    plt.savefig(f'./static/img/{name}.jpg',dpi=200)

def main():
    name="Orange"
    name1="flower"
    name2="m"
    font="msyh.ttc"
    font1="msyh.ttc"
    font2="msyh.ttc"
    name3="tree"
    font3 = "msyh.ttc"
    wc(name,font)
    wc(name1,font1)
    wc(name2,font2)
    wc(name3,font3)


if __name__ == '__main__':
    main()
    print("over")
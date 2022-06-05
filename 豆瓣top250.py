import requests
import re
import copy
import xlwt
from bs4 import BeautifulSoup
import time
import sqlite3
proxies = {
    "http": "http://47.92.113.71:80"
}

header = {
    'user-Agent': 'Mozilla/5.0(Windows NT 10.0;Win64 x64)AppleWebkit/537.36(KHTML,like Gecko) chrome/58.0.3029.110 Safari/537.36'
}
# 影片详情链接
findLink = re.compile(r'<a href="(.*?)">')
# 影片图片
findImgSrc = re.compile(r'<img.*src="(?P<imgsrc>.*?)" ', re.S)
# 影片名字
findTitle = re.compile(r'<span class="title">(.*?)</span>')
# 影片评分
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# 影片评分人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 影片标语
findInq = re.compile(r'<span class="inq">(.*?)</span>')
# 影片导演
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)
# 制片国家
findCts=re.compile(r' / (.*?) / ')    #！！！要以实际输出的div为例寻找正则表达式
# 方法二：制片国家的正则式 二次访问
findCt=re.compile(r'<span class="pl">制片国家/地区:</span>(.*?)<br/>')

def main():
    dbUrl = "https://movie.douban.com/top250?start="
    datalist = getData(dbUrl)
    # savedatalist(datalist)
    # datalist=readdatalist()
    # savePath = "豆瓣top250.xls"
    dbPath = "movie.db"
    #saveData(datalist, savePath)
    saveData2DB(datalist, dbPath)
    # countrys=getCountry(datalist)  #二次访问
    # savecountry(countrys)    #二次访问

def readdatalist():
    datalist=[]
    with open("datalist.txt",mode="r",encoding="utf-8") as f:
        words=f.readlines()
        datalist=words
    print(datalist)
    return datalist

def savedatalist(datalist):
    with open("datalist.txt",mode='w',encoding='utf-8') as f:
        for data in datalist:
            data=str(data)
            f.write(data+'\n')
        print("over!")

def getData(dbUrl):
    datalist = []
    for url in Create_Url(dbUrl):
        # print(url)
        html = AskUrl(url)
        time.sleep(0.3)
        page = BeautifulSoup(html, "html.parser")  # 把响应的返回的页面代码交给BeautifulSoup处理
        divlist = page.find_all("div", class_="item")

        # print(divlist)
        for div in divlist:
            data = []
            div = str(div)
            # print(div)
            link = re.findall(findLink, div)[0]
            data.append(link)
            imgSrc = re.findall(findImgSrc, div)[0]
            data.append(imgSrc)
            title = re.findall(findTitle, div)
            # print(title)
            if len(title) == 2:
                ctitle = title[0]
                data.append(ctitle)
                otitle = title[1].replace("/", "")
                otitle = "".join(otitle.split())
                data.append(otitle)
            else:
                data.append(title[0])
                data.append('  ')
            # print(ctitle)
            rating = re.findall(findRating, div)[0]
            data.append(rating)
            judgenNum = re.findall(findJudge, div)[0]
            data.append(judgenNum)
            inq = re.findall(findInq, div)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append("  ")
            bd = re.findall(findBd, div)[0]
            bd = str(bd)
            # 第一个问号是无论br里有没有空格都匹配，第二个可加可不加？，因为一定有空格，第一个可能没有空格所以加
            bd = re.sub("<br(\\s+)?/>(\\s+)", " ", bd)
            bd = re.sub("/", " ", bd)
            # print(bd.strip())
            data.append(bd.strip())
            ct=re.findall(findCts,div)[0].replace("中国香港","中国").replace("中国大陆","中国").replace("中国台湾","中国").split(' ')[0]
            data.append(ct)
            datalist.append(data)  # 处理好的一部电影信息放入datalist
            # print(link)
    # for i in datalist:
    #     print(i)
    # print(datalist)
    return datalist

def Create_Url(url):
    task = []
    for i in range(10):
        target_url = url + str(i * 25)  # url是字符串类型所以要将数字类型转换
        task.append(target_url)
    return task


def AskUrl(url):
    resp = requests.get(url, headers=header, proxies=proxies)
    return resp.text

def getCountry(datalist):
    countrys=[]
    for data in datalist:
        url=data[0]
        # print(url)
        html=AskUrl(url)
        # print(html)
        page=BeautifulSoup(html,"html.parser")
        div = page.find_all("div",id="info")
        div=str(div)
        # print(div)
        country=re.findall(findCt,div)[0].split('/')[0].strip()
        # print(country)
        countrys.append(country)
    # print(countrys)
    return countrys

def countrydb():
    sql = '''
            create table countrys
            (
                country text
            )
        '''
    conn = sqlite3.connect("country.db")
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

def savecountry(countrys):
    countrydb()
    conn=sqlite3.connect("country.db")
    cur=conn.cursor()
    for country in countrys:
        # print(type(country))
        country=country[0]
        sql='''
            insert into countrys value(%s)'''%(country)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def saveData(datalist, savePath):
    row_num = 0  # 记录写入行数
    col_list = []  # 记录每行宽度
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheel = book.add_sheet('豆瓣250', cell_overwrite_ok=True)
    col_num = [0 for x in range(0, len(datalist))]
    col = ("电影详情链接", "图片链接", "影片中文名", "影片外国名", "评分", "评价数", "概况", "相关信息")
    for i in range(0, 8):
        sheel.write(0, i, col[i])
    for i in range(0, len(datalist[0:])):
        #print("第%d条" % (i + 1))
        data = datalist[i]
        for j in range(0, 8):
            sheel.write(i + 1, j, data[j])
            # 计算每列值的大小
            # print(len(data[j].encoding('utf-8')))
            col_num[j] = len(data[j])
            # print(col_num[j])
        # 记录一行每列的长度
        col_list.append(copy.copy(col_num))
        row_num += 1

    col_max_num = get_max_col(col_list)
    for i in range(0, len(col_max_num)):
        sheel.col(i).width = 256 * (col_max_num[i] + 2)
    book.save(savePath)


def saveData2DB(datalist, dbPath):
    init_db(dbPath)
    conn=sqlite3.connect(dbPath)
    cur=conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            if index==4 or index==5:
                continue
            data[index]='"'+str(data[index])+'"'
        sql='''
        insert into movie250(
        info_link,pic_link,cname,ename,score,rated,introduction,info,country)
        values(%s)'''%",".join(data)        #如果是二次访问的话没有country
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()


def init_db(dbPath):
    sql ='''
        create table movie250
        (
        id integer primary key autoincrement,
        info_link text,
        pic_link text,
        cname varchar ,
        ename varchar ,
        score numeric,
        rated numeric,
        introduction text,
        info text,
        country text
        )
    '''  #如果是二次访问的话没有country
    conn = sqlite3.connect(dbPath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


def get_max_col(max_list):
    line_list = []
    # i代表每行，j代表每列
    for j in range(0, 8):
        line_num = []
        for i in range(len(max_list)):
            line_num.append(max_list[i][j])  # 将每列的宽度存入line_num
        line_list.append(max(line_num))
        print(line_list)
    return line_list

main
if __name__ == '__main__':
    main()
    print("爬取完毕")

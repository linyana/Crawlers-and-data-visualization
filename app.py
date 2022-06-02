from flask import Flask, render_template
import sqlite3
import jieba

app = Flask(__name__)
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'

def con_databaes():
    datalist = []
    con = sqlite3.connect("movie.db")
    cur = con.cursor()
    sql = "select * from movie250"
    data = cur.execute(sql)
    for i in data:
        datalist.append(i)
    cur.close()
    con.close()
    return datalist


def Cloud():
    conn = sqlite3.connect('movie.db')
    cur = conn.cursor()
    sql = 'select introduction from movie250'
    data = cur.execute(sql)
    text = ""
    for item in data:
        text = text + item[0]
    # print(text)
    cur.close()
    conn.close()

    cut = jieba.cut(text)
    string = ' '.join(cut)
    return string


@app.route('/')
def index():  # put application's code here
    cloud = Cloud()
    datalist=con_databaes()
    return render_template("index.html", cloud=len(cloud),movie_len=len(datalist))


@app.route('/index')
def home():  # put application's code here
    cloud = Cloud()
    datalist = con_databaes()
    return render_template("index.html", cloud=len(cloud), movie_len=len(datalist))

@app.route('/cloud')
def cloud():  # put application's code here
    return render_template("cloud.html")

@app.route('/movie')
def movie():  # put application's code here
    datalist = con_databaes()
    return render_template("movie.html", movies=datalist)


@app.route('/score')
def score():  # put application's code here
    datalist = con_databaes()
    return render_template("score.html", movies=datalist)




if __name__ == '__main__':
    app.run()

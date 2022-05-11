from flask import Flask, render_template, request, redirect, url_for
import connect
from sql import db
from user import User
import sqlite3

app = Flask(__name__)
app.config.from_object(connect)
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')
        user = User.query.filter_by(username=username).first()
        if not username:
            return render_template('register.html', msg='填写不完整！')
        elif not password or not repassword:
            return render_template('register.html', msg='填写不完整！')
        elif user:
            return render_template('register.html', msg='用户已存在！')
        if password == repassword:
            user = User()
            user.username = username
            user.password = password
            db.session.add(user)
            db.session.commit()
            return render_template('login.html', msg='注册成功，请登录！')
        else:
            return render_template('register.html', msg='密码不一致！')
    return render_template('register.html')


# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        res = {}
        # 检测用户名
        if not user:
            return render_template('login.html', msg='填写不完整！')
        # 检测密码
        if user.password != password:
            return render_template('login.html', msg='密码不正确！')
        if user.flag == 1:
            users = User.query.filter_by(flag=0)
            return render_template('admin.html', users=users)
        else:
            return render_template('index.html', user=user)
    return render_template('login.html')


@app.route('/delete')
def delete():
    id = request.args.get('id')
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    users = User.query.filter_by(flag=0)
    return render_template('admin.html', users=users)


# 用户修改
@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        id = request.form.get('id')
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.get(id)
        user.username = username
        user.password = password
        db.session.commit()
        users = User.query.filter_by(flag=0)
        return render_template('admin.html', users=users)
    else:
        id = request.args.get('id')
        users = User.query.get(id)
        return render_template('update.html', users=users)


@app.route('/index')
def home():
    return render_template("index.html")


@app.route('/tea')
def tea():
    datalist = []
    con = sqlite3.connect("tea.db")
    cur = con.cursor()
    sql = "select * from TB_TEA"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    return render_template("tea.html", tea=datalist)


@app.route('/milk')
def milk():
    datalist = []
    con = sqlite3.connect("milk.db")
    cur = con.cursor()
    sql = "select * from TB_TEA"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()
    return render_template("milk.html", tea=datalist)


@app.route('/score')
def score():
    score = []  # 评分
    num = []  # 每个区域所统计出的店铺数量
    con = sqlite3.connect("tea.db")
    cur = con.cursor()
    sql = "select address, count(name) cnt from TB_TEA group by address"
    data = cur.execute(sql)
    for item in data:
        score.append(str(item[0]))
        num.append(item[1])

    score1 = []  # 评分
    num1 = []  # 每个店铺所统计出的评论数量
    cur1 = con.cursor()
    sql1 = "select distinct name, number from TB_TEA order by number desc limit 20"
    data1 = cur1.execute(sql1)
    for item in data1:
        score1.append(str(item[0]))
        num1.append(item[1])

    score2 = []  # 评分
    num2 = []  # 每个店铺所统计出的评论数量
    cot = sqlite3.connect("milk.db")
    cur2 = cot.cursor()
    sql2 = "select address, count(name) cnt from TB_TEA group by address"
    data2 = cur2.execute(sql2)
    for item in data2:
        score2.append(str(item[0]))
        num2.append(item[1])

    score3 = []  # 评分
    num3 = []  # 每个店铺所统计出的评论数量
    cur3 = cot.cursor()
    sql3 = "select distinct name, number from TB_TEA order by number desc limit 20"
    data3 = cur3.execute(sql3)
    for item in data3:
        score3.append(str(item[0]))
        num3.append(item[1])

    cur.close()
    cur1.close()
    cur2.close()
    cur3.close()
    con.close()
    cot.close()
    return render_template("charts.html", score=score, num=num, score1=score1, num1=num1, score2=score2, num2=num2,
                           score3=score3, num3=num3)


@app.route('/word')
def word():
    return render_template("word.html")


@app.route('/team')
def team():
    datalist = []
    datalist1 = []
    con = sqlite3.connect("tea.db")
    cur = con.cursor()
    sql = "select * from retea"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)

    con1 = sqlite3.connect("milk.db")
    cur1 = con1.cursor()
    sql1 = "select * from remilk"
    data1 = cur1.execute(sql1)
    for item1 in data1:
        datalist1.append(item1)
    cur.close()
    cur1.close()
    con.close()
    con1.close()
    return render_template("recommend.html", tea=datalist, milk=datalist1)

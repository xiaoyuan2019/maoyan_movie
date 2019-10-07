from flask import Flask, render_template, url_for, request, jsonify, redirect, session, Markup
import config  # 导入配置文件
from exts import db  # 导入db
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, validators
from models import Action2019, TOP100, Comedy2019, MovieDetail  # 导入模型
from spider_movie import MovieSpider  # 导入爬虫类
from PIL import ImageFont, Image, ImageDraw
import random


app = Flask(__name__)  # 初始化app
app.config.from_object(config)  # 用于关联config文件
app.config['SECRET_KEY'] = 'foxconn'  # 设置flask 秘钥
db.init_app(app)  # 初始化db

'''
1. session数据是保存到后端的数据库中;
2.session中的从狭义和广义上分：
  （1）session，广义上 :是一种机制：在前端当中存一个session_id ,在后端当中去保存这份session的属性值，然后访问的时候只要能够带上这份session_id
的值，就可以知道之前保存的数据是什么。整个的这种机制，是一种session机制
  （2）session，狭义上 ：只是仅仅保存到后端的session数据
3. 在设置使用session时,必须要做一个配置,即flask的session中需要用到的秘钥字符串，可以是任意值
    app.config["SECRET_KEY"] = "任意的字符串";
4. 如果没有设置session时，获取到的session就是None;
'''
@app.route('/')
def index1():
	return render_template('index.html')

@app.route('/index')
def index():
	return render_template('index.html')

# 自定义JinJia2过滤器
@app.template_filter('str_list')
def str_list(args):
	temp = args.split('&&&')
	# print(temp)
	return temp

@app.route('/detail/<mid>')
def detail(mid):
	# 从数据库抓取电影详情
	detail_info = MovieDetail.query.filter_by(detail_id=mid).first()
	return render_template('detail.html', data=detail_info)


@app.route('/add_comment', methods=['GET', 'POST'])
def add_comment():
	# 获取前端传回的信息
	content = request.form.get('movie_comment')
	mid = request.form.get('mid')
	# print(content, mid)
	# 查询对应电影信息
	detail_obj = MovieDetail.query.filter_by(detail_id=mid).first()
	old_comment = detail_obj.comment
	detail_obj.comment = old_comment + '&&&' + content  # 评论拼接，并存入DB
	db.session.commit()
	return jsonify('OK')

@app.errorhandler(404)
def page404(e):
	return '对不起，您访问的页面不存在，请确认！！！'

@app.errorhandler(405)
def page405(e):
	return '对不起，您访问的页面仅支持GET请求，不支持POST请求，请确认！！！'

@app.teardown_request
def server_teardown_request(e):
	return '对不起，服务器出现错误，错误信息是：{}'.format(str(e))

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	# POST请求，获取前端传过来的数据
	msg_dict = {'status': True, 'msg': None}  # 返回信息
	username = request.form.get('username')
	password = request.form.get('password')
	if username and password:
		if username == 'xiaoyuan' and password == 'fhwsie':
			msg_dict['msg'] = '登录成功'
			session['is_login'] = True  # 储存用户登录状态
			session['user'] = username   # 储存用户登录名称
			# print('登录成功')
			return jsonify(msg_dict)
			# return redirect(url_for('index'))
		else:
			msg_dict['status'] = False
			msg_dict['msg'] = '用户名或密码错误'
			return jsonify(msg_dict)
	else:
		msg_dict['status'] = False
		msg_dict['msg'] = '用户名和密码必须填写！'
		return jsonify(msg_dict)

@app.route('/login')
def logout():
	session.clear()   # 清除所有会话
	return redirect(url_for('login'))

@app.route('/top100/')
def top100():
	page = request.args.get('page', 1, type=int)
	# 获取TOP100电影数据
	# top100_info = TOP100.query.all()   # 从数据库抓取数据
	top100_info = TOP100.query.order_by(TOP100.top.asc()).paginate(page=page, per_page=9)
	# top100_info = MovieSpider('TOP100').get_data()  # 实时抓取数据
	return render_template('top100.html', data=top100_info.items, pagination=top100_info)

@app.route('/action2019/')
def action2019():
	page = request.args.get('page', 1, type=int)  # GET请求获取前端分页url中的page参数的值
	action2019_info = Action2019.query.order_by(Action2019.id.asc()).paginate(page=page, per_page=12)  # 数据库获取电影信息
	return render_template('action2019.html', data=action2019_info.items, pagination=action2019_info)
	# action2019_info = MovieSpider('action2019').get_data()  # 实时爬取电影信息


@app.route('/comedy2019/')
def comedy2019():
	page = request.args.get('page', 1, type=int)  # 获取前端分页url中的page参数的值
	comedy2019_info = Comedy2019.query.order_by(Comedy2019.id.asc()).paginate(page=page, per_page=12)  # 数据库获取电影信息
	return render_template('comedy2019.html', data=comedy2019_info.items, pagination=comedy2019_info)
	# comedy2019_info = MovieSpider('comedy2019').get_data()  # 实时爬取电影信息


if __name__ == '__main__':
	# 启动flask虚拟的应用服务器，来持续监听用户的请求，相当于while true:
	app.run()

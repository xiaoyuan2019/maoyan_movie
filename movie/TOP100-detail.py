import requests
from lxml import etree
import pymysql, re, json
from pyquery import PyQuery as pq

headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

def get_HTMLcontent(url):
	try:
		dom = pq(url, headers=headers, timeout=30)
		return dom
	except:
		return '获取网页内容异常'


def parse_html(dom):
	movie_info = {}  # 存储每部电影的详情，用于存储至DB
	movie_id = []  # 存储每部电影的详情id
	# pyquery获取电影详情a标签中的id
	result = dom('p.name a')  # 获取每部电影的详情id，后面会与https://maoyan.com/ 做拼接
	for item in result.items():
		# print(item.attr('href'))
		movie_id.append(item.attr('href'))
	# print(movie_id)
	# 通过pyquery循环获取每部电影详情页面的电影简介、主演、主演图片url、评论
	for item in movie_id:
		movie_id = item.split('/')[-1]
		url = 'https://maoyan.com' + item
		# print(url)
		detail = pq(url, headers=headers)
		title = detail('.movie-brief-container h3.name').text()  # 电影名称
		title_img = detail('.avatar-shadow img').attr('src')  # 电影图片url
		introduction = detail('.mod-content span.dra').text()  # 电影简介
		director = detail('.celebrity-group').eq(0)('.info a').text()  # 导演
		director_img = detail('.celebrity-group').eq(0)('a.portrait img').attr('data-src')  # 导演照片url
		actors = detail('.celebrity-group').eq(1)('li')  # 演员信息
		actor_list = []
		actor_role_list = []
		actor_img_list = []
		for actor in actors.items():
			actor_img_list.append(actor('.portrait img').attr('data-src'))  # 演员照片url
			actor_list.append(actor('.info a').text())  # 演员列表
			actor_role_list.append(actor('.info span').text())  # 演员角色列表
		# 为了便于数据库存储与前端展示，这里将每部电影有多个值的信息比如演员、评论等都用&&&连接成字符串
		# 存入数据库，并在前端显示时，利用jinjia2模板语言的过滤器按照&&&进行分隔显示
		actor = '&&&'.join(actor_list)
		actor_role = '&&&'.join(actor_role_list)
		actor_img = '&&&'.join(actor_img_list)
		# print(actor)
		# print(actor_role)
		# print(actor_img)
		comments = detail('li.comment-container')
		comment_user_list = []
		comment_time_list = []
		comment_content_list = []
		for item in comments.items():
			comment_user_list.append(item('.main .user span.name').text())  # 评论人账号
			comment_time_list.append(item('.main .time span').text())  # 评论人日期
			comment_content_list.append(item('.main .comment-content').text())  # 评论内容
		comment_user = '&&&'.join(comment_user_list)
		comment_time = '&&&'.join(comment_time_list)
		comment_content = '&&&'.join(comment_content_list)
		# 将每部电影的信息存入数据库
		# print(item)
		movie_info['title'] = title
		movie_info['title_img'] = title_img
		movie_info['movie_id'] = movie_id
		movie_info['introduction'] = introduction
		movie_info['director'] = director
		movie_info['director_img'] = director_img
		movie_info['actor'] = actor.replace('\'', '')
		movie_info['actor_img'] = actor_img
		movie_info['actor_role'] = actor_role.replace('\'', '')
		movie_info['comment'] = comment_content.replace('\'', '')
		movie_info['comment_user'] = comment_user.replace('\'', '')
		movie_info['comment_time'] = comment_time
		# 存入数据库
		# for k,v in movie_info.items():
		# 	print('{}:{},{}'.format(k,v,type(v)))
		save_to_db(movie_info)

def save_to_db(info):
	conn = pymysql.connect(host='10.195.251.148', port=3306,
	                       user='root', passwd='fhwsie', db='maoyan', charset='utf8')
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
	cursor.execute("insert into moviedetail (title, title_img, detail_id, introduction, director, \
	director_img, actor, actor_img, actor_role, comment, comment_user, comment_time) \
     values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}')".format(
		info['title'],
		info['title_img'],
		info['movie_id'],
		info['introduction'],
		info['director'],
		info['director_img'],
		info['actor'],
		info['actor_img'],
		info['actor_role'],
		info['comment'],
		info['comment_user'],
		info['comment_time']
	))
	conn.commit()
	cursor.close()
	conn.close()


def delete_table_data():
	conn = pymysql.connect(host='10.195.251.148', port=3306,
	                       user='root', passwd='fhwsie', db='maoyan', charset='utf8')
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
	cursor.execute("delete from moviedetail;")
	conn.commit()
	cursor.close()
	conn.close()

if __name__ == '__main__':
	# 运行脚本之前，先清空表中数据，避免数据重复，保证电影信息是最新的
	delete_table_data()
	for i in range(10):
		# 豆瓣每一页显示25部电影，每一页的页面url是第一部电影的序号
		url = 'https://maoyan.com/board/4?offset={}'.format(i * 10)
		parse_html(get_HTMLcontent(url))  # 解析网页内容，获取电影信息

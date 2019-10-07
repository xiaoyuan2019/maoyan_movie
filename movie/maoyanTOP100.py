import requests
from lxml import etree
import pymysql, re, json
from pyquery import PyQuery as pq

headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

def get_HTMLcontent(url):
	try:
		r = requests.get(url, headers=headers, timeout=30).text  # 模拟浏览器抓取url网页内容
		s = etree.HTML(r)
		return s
	except:
		return '获取网页内容异常'


def parse_html(s):
	# 利用xpath解析网页信息
	top = s.xpath('//dd/i/text()')  # top排行
	img = s.xpath('//a[@class="image-link"]/img[2]/@data-src')  # 电影图片url
	title = s.xpath('//p[@class="name"]/a/text()')  # 电影名
	movie_detail = s.xpath('//p[@class="name"]/a/@data-val')  # 获取每部电影的详情id，后面会与https://maoyan.com/films/id 做拼接
	actor = s.xpath('//p[@class="star"]/text()')  # 主演
	movie_time = s.xpath('//p[@class="releasetime"]/text()')  # 电影上映日期
	score1 = s.xpath('//p[@class="score"]/i[1]/text()')  # 评分1
	score2 = s.xpath('//p[@class="score"]/i[2]/text()')  # 评分2
	score = [i + j for i, j in zip(score1, score2)]  # 评分拼接
	# print(movie_detail, len(movie_detail))
	# print(top,len(top))
	# print(img,len(img))
	# print(title, len(title))
	# print(actor,len(actor))
	# print(movie_time,len(movie_time))
	# print(score,len(score))

	# 处理电影详情id，以及抓取电影详情
	movie_id = [item.replace('}', '').split(':')[-1] for item in movie_detail]
	# 通过yield生成器，将电影的6个信息一一对应起来形成字典格式，并逐一返回，前提是各信息列表的长度一致
	for i in range(len(top)):
		yield {
			'top': top[i],
			'img': img[i],
			'title': title[i],
			'detail_id': movie_id[i],
			'actor': actor[i].replace('\n', '').strip(),
			'release_time': movie_time[i],
			'score': score[i],
		}

def save_to_db(info):
	conn = pymysql.connect(host='10.195.251.148', port=3306,
	                       user='root', passwd='fhwsie', db='maoyan', charset='utf8')
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
	cursor.execute("insert into top100 (top,title,actor,release_time,score,img,detail_id) \
     values ('{0}','{1}','{2}','{3}','{4}','{5}', '{6}')".format(info['top'], \
	                                                      info['title'], info['actor'], info['release_time'],
	                                                      info['score'], info['img'], info['detail_id']))
	conn.commit()
	cursor.close()
	conn.close()


def delete_table_data():
	conn = pymysql.connect(host='10.195.251.148', port=3306,
	                       user='root', passwd='fhwsie', db='maoyan', charset='utf8')
	cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
	cursor.execute("delete from top100;")
	conn.commit()
	cursor.close()
	conn.close()


def save_to_txt(content):
	with open('movie.txt', 'a', encoding='utf-8') as f:
		f.write(json.dumps(content, ensure_ascii=False) + '\n')
		f.write('=' * 50 + '\n')


if __name__ == '__main__':
	# 运行脚本之前，先清空表中数据，避免数据重复，保证电影信息是最新的
	delete_table_data()
	for i in range(5):
		# 豆瓣每一页显示25部电影，每一页的页面url是第一部电影的序号
		url = 'https://maoyan.com/board/4?offset={}'.format(i * 10)
		result = parse_html(get_HTMLcontent(url))  # 解析网页内容，获取电影信息
		for item in result:
			# print(item)
			# 写入txt文件
			# save_to_txt(item)
			# 写入数据库
			save_to_db(item)

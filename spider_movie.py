import requests
from lxml import etree
from exts import db
from models import TOP100, Action2019, Comedy2019

class MovieSpider():
	def __init__(self, movie_type, page_num=2):
		self.movie_info = []
		self.movie_type = movie_type  # 由主程序传入需要爬取电影的类型
		self.url = None
		self.page_moive_num = 30  # 网页分页偏移量offset
		self.page_num = page_num  # 由主程序传入需要爬取的页数
		if self.movie_type == 'TOP100':
			self.url = 'https://maoyan.com/board/4?offset='
			self.page_moive_num = 10
		elif self.movie_type == 'action2019':
			self.url = 'https://maoyan.com/films?showType=3&catId=5&yearId=14&offset='
		elif self.movie_type == 'comedy2019':
			self.url = 'https://maoyan.com/films?showType=3&catId=2&yearId=14&offset='

	def get_page(self, url):
		headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
		try:
			r = requests.get(url, headers=headers, timeout=30).text
			s = etree.HTML(r)
			return s
		except:
			return '获取网页内容异常'

	def parse_common_page(self, data):
		movie_list = data.xpath('//div[@class="movies-channel"]//dd')  # 相对路径，定位class为movie-list的d1标签
		title_list = []
		img_list = []
		score_list = []
		# 循环每个dd标签，使用xpath获取相关信息，并加入对应列表中
		for item in movie_list:
			title = item.xpath('./div[2]/a/text()')[0]  # 绝对路径，获取当前dd标签内的第二个div下面的a标签的内容，即电影名称
			title_list.append(title)
			# //*[@id="app"]/div/div[2]/div[2]/dl/dd[3]/div[1]/a/div/img[2]
			img = item.xpath('./div[1]/a/div/img[2]/@data-src')[0]  # 电影图片url
			img_list.append(img)
			score_tmp = item.xpath('./div[3]/text()')  # 绝对路径，获取评分div是否有评分
			if '暂无评分' in score_tmp:
				score_list.append('暂无评分')
			else:
				score1 = item.xpath('./div[3]/i[1]/text()')  # 绝对路径，第一个评分
				score2 = item.xpath('./div[3]/i[2]/text()')  # 绝对路径，第二个评分
				score = [i + j for i, j in zip(score1, score2)]
				score_list.extend(score)
		# 通过yield生成器，将电影的3个信息一一对应起来形成字典格式，并逐一返回，前提是各信息列表的长度一致
		for i in range(len(title_list)):
			yield {
				'img': img_list[i],
				'title': title_list[i].replace("'", ' '),  # 替换掉单引号，避免存入数据库时产生语法错误
				'score': score_list[i],
			}

	def parse_top100_page(self, data):
		top = data.xpath('//dd/i/text()')  # top排行
		img = data.xpath('//a[@class="image-link"]/img[2]/@data-src')  # 电影图片url
		title = data.xpath('//p[@class="name"]/a/text()')  # 电影名
		actor = data.xpath('//p[@class="star"]/text()')  # 主演
		movie_time = data.xpath('//p[@class="releasetime"]/text()')  # 电影上映日期
		score1 = data.xpath('//p[@class="score"]/i[1]/text()')  # 评分1
		score2 = data.xpath('//p[@class="score"]/i[2]/text()')  # 评分2
		score = [i + j for i, j in zip(score1, score2)]  # 评分拼接
		# 通过yield生成器，将电影的6个信息一一对应起来形成字典格式，并逐一返回，前提是各信息列表的长度一致
		for i in range(len(top)):
			yield {
				'top': top[i],
				'img': img[i],
				'title': title[i],
				'actor': actor[i].replace('\n', '').strip(),
				'release_time': movie_time[i],
				'score': score[i],
			}

	def save_top100_to_db(self, data):
		for item in data:
			top100 = TOP100(top=item.top, title=item.title, actor=item.actor, release_time=item.release_time, score=item.score, img=item.img)
			db.session.add(top100)
			db.session.commit()

	def save_action2019_to_db(self, data):
		for item in data:
			action2019 = Action2019(title=item.title, score=item.score, img=item.img)
			db.session.add(action2019)
			db.session.commit()

	def save_comedy2019_to_db(self, data):
		for item in data:
			comedy2019 = Comedy2019(title=item.title, score=item.score, img=item.img)
			db.session.add(comedy2019)
			db.session.commit()

	def get_data(self):
		for i in range(self.page_num):
			wb_url = self.url + '{}'.format(i * self.page_moive_num)
			if self.movie_type == 'TOP100':
				res = self.parse_top100_page(self.get_page(wb_url))
				# self.save_top100_to_db(res)
			elif self.movie_type == 'action2019':
				res = self.parse_common_page(self.get_page(wb_url))
				# self.save_action2019_to_db(res)
			elif self.movie_type == 'comedy2019':
				res = self.parse_common_page(self.get_page(wb_url))
				# self.save_comedy2019_to_db(res)
			self.movie_info.extend(res)  # 将生成器返回的每一条数据追加到全局变量中
		return self.movie_info  # 将电影信息列表返回给主程序渲染页面

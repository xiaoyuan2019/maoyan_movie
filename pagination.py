from flask import Markup

class Pagination:
	def __init__(self, request, sum_num, per_num=5, max_show=11):
		# 获取前端传回的页码数，做异常捕获，如果找不到key page，就使用默认值1；
		# 如果获取page出现任何异常，使用页码1
		# 如果当前page<=0，使用页码1
		try:
			self.current_page = int(request.get('page', 1))
			if self.current_page <= 0:
				self.current_page = 1
		except Exception as e:
			self.current_page = 1
		# print("当前页码：", self.current_page)
		#获取基础URL，便于分页器移植到其他页面使用
		self.base_url = request.path
		# 每一页固定显示的数据：10条
		self.per_num = per_num
		# 总共的数据条目
		self.sum_num = sum_num
		# print("总的数据量：", self.sum_num)
		# 总共的页码数
		self.sum_page, more = divmod(self.sum_num, self.per_num)
		if more:
			self.sum_page += 1  # 当不能整除时，总页码数要加1
		# print("总的页码数：", self.sum_page)
		# 最大显示页码：11
		self.max_show = max_show
		half_show = max_show // 2
		# 页码对称判断，左边5个右边5个中间1个
		# 当总页码数小于等于最大显示页码数时：只显示最大显示页码
		if self.sum_page <= max_show:
			self.page_start = 1
			self.page_end = self.sum_page
		else:
			# 当总页码数大于最大显示页码数时：最大显示11个页码，要控制好左边和右边的页码溢出情况，否则会出现负页码数和无效页码数
			# 因此这里要判断当前页码-5和+5的边界问题
			if self.current_page <= half_show:
				self.page_start = 1
				self.page_end = max_show
			elif self.current_page + max_show > self.sum_page:
				self.page_start = self.sum_page - max_show + 1
				self.page_end = self.sum_page
			else:
				self.page_start = self.current_page - half_show
				self.page_end = self.current_page + half_show
	# 对原数据进行切片，计算开始和终止值
	'''
	第一页：0-5
	第二页：5-10
	第三页：10-15
	'''
	@property
	def get_start(self):
		return  (self.current_page - 1) * self.per_num
	@property
	def get_end(self):
		return  self.current_page * self.per_num
	@property
	def gen_li(self):
		# 在后端生成页码html标签，循环加入到列表中，然后join成字符串返回到前端
		html_list = []
		# 增加首页功能
		first_li = '<li><a href="{}?page=1">首页</a></li>'.format(self.base_url)
		html_list.append(first_li)
		# 增加上一页功能
		if self.current_page == 1:
			prev_li = '<li class="disabled"><a><<</a></li>'
		else:
			prev_li = '<li><a href="{1}?page={0}"><<</a></li>'.format(self.current_page - 1,self.base_url)
		html_list.append(prev_li)
		# 在前端显示11个页码数
		for page in range(self.page_start, self.page_end + 1):
			# 判断当前页是否为点击页码，是的话就加上active属性
			if self.current_page == page:
				html_li = '<li class="active"><a href="{1}?page={0}">{0}</a></li>'.format(page,self.base_url)
			else:
				html_li = '<li><a href="{1}?page={0}">{0}</a></li>'.format(page,self.base_url)
			html_list.append(html_li)
		# 增加下一页功能
		if self.current_page == self.sum_page:
			next_li = '<li class="disabled"><a>>></a></li>'
		else:
			next_li = '<li><a href="{1}?page={0}">>></a></li>'.format(self.current_page + 1,self.base_url)
		html_list.append(next_li)
		# 增加尾页功能
		last_li = '<li><a href="{1}?page={0}">尾页</a></li>'.format(self.sum_page,self.base_url)
		html_list.append(last_li)
		# 将分页代码join成字符串，并变成安全代码传回前端显示，或者在前端使用模板语言{{ html_str|safe }}也行
		return Markup(''.join(html_list))

from flask import Flask,render_template,url_for
import config        # 导入配置文件
from exts import db   # 导入db
from models import Action2019,Comedy2019,TOP100   # 导入模型

app = Flask(__name__)
app.config.from_object(config)  # 用于关联config文件
db.init_app(app)   # 初始化db

# 使用了flask-migrate库后，就不需要这样应用模型到数据库了，有专门的命令来执行
# 解决app上下文问题
# with app.app_context():
# 	db.create_all()

# 浏览器根据url后缀查找对应装饰器指定的路由，如果匹配，随即执行该装饰器紧挨着的业务函数，并由该函数
# 返回字符串或模板到前端页面渲染展示给用户看。
# flask路由系统默认只支持GET请求，如需支持POST，需添加参数methods进行指定
@app.route('/maoyan', methods=['GET', 'POST'])
def maoyan():
	# 新增数据
	# top100 = TOP100(top='1', title='霸王别姬', actor='张国荣，张丰毅，巩俐', release_time='1993-9-1', score='9.7',
	#                 img='http://234ssdkfj234lsdfl.png')
	# db.session.add(top100)
	# db.session.commit()

	# 查数据
	# top100 = TOP100.query.filter(TOP100.top == '1').first()  # 取出列表第一个元素
	# print(type(top100))
	# print(top100.top, top100.title, top100.actor, top100.release_time, top100.score)

	# 改数据
	# top100 = TOP100.query.filter(TOP100.top == '1').first()
	# top100.release_time = '1997-9-1'
	# db.session.commit()

	# 删数据
	# top100 = TOP100.query.filter(TOP100.top == '1').first()
	# db.session.delete(top100)
	# db.session.commit()

	# 多对多查询
	article = Article.query.filter(Article.title == 'cisco')
	tags = article.tags  # 查找文章cisco所对应的所有tag
	for tag in tags:
		print(tag)

	return '猫眼电影TOP100'

@app.route('/index')
def index():
	a = ['TOP100', '国内票房榜', '2019动作电影', '2019科幻电影', '2019喜剧电影']
	return render_template('index.html', result=a) # 返回列表到前端显示，使用flask核心组件jinjia2模板语言处理

@app.route('/')
def login():
	return render_template('login2.html')

if __name__ == '__main__':
	# 启动flask虚拟的应用服务器，来持续监听用户的请求，相当于while true:
	app.run()

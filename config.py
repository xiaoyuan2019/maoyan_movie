# 设置数据库连接参数，标准格式：dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = 'fhwsie'
HOST = '10.195.251.148'
PORT = '3306'
DATABASE = 'maoyan'
# 字符串拼接
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format\
	(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# # 设置flask secret_key
# app.config['secret_key'] = 'foxconn'
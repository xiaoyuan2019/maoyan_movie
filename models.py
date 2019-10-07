from exts import db

# 创建ORM表
class Comedy2019(db.Model):
	__tablename__ = 'comedy2019'  # 喜剧2019，设置表名
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(32), nullable=False)
	detail_id = db.Column(db.String(32), nullable=False)
	score = db.Column(db.String(32), nullable=False)
	img = db.Column(db.String(100), nullable=False)
class Action2019(db.Model):
	__tablename__ = 'action2019'  # 动作2019，设置表名
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	title = db.Column(db.String(32), nullable=False)
	detail_id = db.Column(db.String(32), nullable=False)
	score = db.Column(db.String(32), nullable=False)
	img = db.Column(db.String(100), nullable=False)
class TOP100(db.Model):
	__tablename__ = 'top100'  # TOP100，设置表名
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	top = db.Column(db.Integer, nullable=False)
	title = db.Column(db.String(32), nullable=False)
	detail_id = db.Column(db.String(32), nullable=False)
	actor = db.Column(db.String(32), nullable=False)
	release_time = db.Column(db.String(32), nullable=False)
	score = db.Column(db.String(32), nullable=False)
	img = db.Column(db.String(100), nullable=False)
class MovieDetail(db.Model):
	__tablename__ = 'moviedetail'  # MovieDetail，设置表名
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	detail_id = db.Column(db.String(32), nullable=False)
	title = db.Column(db.String(32), nullable=False)
	title_img = db.Column(db.String(100), nullable=False)
	introduction = db.Column(db.Text, nullable=False)
	director = db.Column(db.String(32), nullable=False)
	director_img = db.Column(db.String(100), nullable=False)
	actor = db.Column(db.String(200), nullable=False)
	actor_role = db.Column(db.String(200), nullable=False)
	actor_img = db.Column(db.Text, nullable=False)
	comment = db.Column(db.Text, nullable=False)
	comment_user = db.Column(db.String(200), nullable=False)
	comment_time = db.Column(db.String(200), nullable=False)

# 多对多关系
# article_tag = db.Table('article_tag',
#                        db.Column('article_id', db.Integer, db.ForeignKey('article.id'), primary_key=True),
#                        db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
#                        )
# class Article(db.Model):
# 	__tablename__ = 'article'
# 	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# 	title = db.Column(db.String(100), nullable=False)
# 	tags = db.relationship('Tag', secondary=article_tag,backref=db.backref('tags')) # 可以查看该文章的所有标签
# class Tag(db.Model):
# 	__tablename__ = 'tag'
# 	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
# 	name = db.Column(db.String(100), nullable=False)


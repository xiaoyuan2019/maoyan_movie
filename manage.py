from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from models import Action2019,Comedy2019,TOP100,MovieDetail  # 必须导入模型中的类名，flask才会知道要增删改查哪个表

# app实例化命令管理类
manager = Manager(app)
# 使用app和db初始化迁移类
migrate = Migrate(app, db)
# 新增上级命令db，并使用MigrateCommand中定义好的子命令，如init\migrate\upgrade等
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()



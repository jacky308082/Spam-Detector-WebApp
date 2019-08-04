"""
flask_script提供可以插入外部腳本的動作 可以在command line對flask進行修改或更新
flask_migrate又分成三個指令
首先要採用MigrateCommand使其可以在command line上運作 ex. python dbModel.py db init 就可以知道是在做migrate
1. python dbModel.py db init依據資料庫的結構進行初始化設定並放在migrations資料夾(versions)裡
2. python dbModel.py db migrate產生資料庫內容
3. python dbModel.py db upgrade來更新資料庫內容
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

db = SQLAlchemy()

class resultData(db.Model):
	__tablename__ = 'db'

	Id = db.Column(db.Integer, primary_key=True)
	document = db.Column(db.String(256))
	result = db.Column(db.String(64))
	createDate = db.Column(db.DateTime)

	def __init__(self, document, result, createDate):
		self.document = document
		self.result = result
		self.createDate = createDate

if __name__ == "__main__": 
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qsjomqlqepfebu:ca900482b474c7141efa487c1d46a1183e08c2d50933e386f9d5df887fe6fb4a@ec2-107-20-185-16.compute-1.amazonaws.com:5432/d4qdnqvkfmbfnd'
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	db = SQLAlchemy(app)
	migrate = Migrate(app,db)

	manager = Manager(app)
	manager.add_command('db', MigrateCommand)
	manager.run()
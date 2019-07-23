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
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/app'
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	db = SQLAlchemy(app)
	migrate = Migrate(app,db)

	manager = Manager(app)
	manager.add_command('db', MigrateCommand)
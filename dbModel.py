from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gsauxupdtlrdxw:570b63e6418005cb3a9df34e84edf0044136a57b1b3705847d29a33415ff734c@ec2-54-243-208-234.compute-1.amazonaws.com:5432/d2od04jmuld6tc'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

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
	manager.run()

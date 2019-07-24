from app import db
import os

class resultData(db.Model):
	__tablename__ = 'spam_db'
	__table_args__ = {'extend_existing': True} 

	Id = db.Column(db.Integer, primary_key=True)
	document = db.Column(db.String(256))
	result = db.Column(db.String(64))
	createDate = db.Column(db.DateTime)

	def __init__(self, document, result, createDate):
		self.document = document
		self.result = result
		self.createDate = createDate

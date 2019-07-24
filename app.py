"""
將由python解釋器執行已運行flask web應用程式的主要代碼
針對消息進行分類
"""

# render_template讓flask可以渲染於網路瀏覽器中
from flask import Flask, jsonify, render_template, url_for, request
# Form形成表單， TextAreaField建立填空欄， validators 驗證表單內容是否符合格式
from wtforms import Form, TextAreaField, validators
from flask_restful import Api, Resource 
import os
import pandas as pd
import numpy as np
import sqlite3
import pickle
#from update import update_model
from dbModel import *
from datetime import datetime

"""
使用__name__可以讓flask知道它可以在同一個目錄底下，找到html模板的文件夾
決定程式的根目錄
"""
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gsauxupdtlrdxw:570b63e6418005cb3a9df34e84edf0044136a57b1b3705847d29a33415ff734c@ec2-54-243-208-234.compute-1.amazonaws.com:5432/d2od04jmuld6tc'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# 準備model
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir, 'pickle_model/classifier.pkl'), 'rb'))
cv = pickle.load(open(os.path.join(cur_dir, 'pickle_model/countvectorizer.pkl'), 'rb'))
#db = os.path.join(cur_dir, 'spam_classification.sqlite')

def predict(document):
	"""
	利用已經建好的模型來預測輸入的資料
	"""
	label = {0: 'not spam', 1: 'spam'}
	# 將其轉成矩陣
	X = cv.transform([document])
	y = clf.predict(X)
	# 預測機率
	proba = np.max(clf.predict_proba(X))
	return label[int(y)], y, proba

def train(document, y):
	"""
	重新訓練模型
	"""
	X = cv.transform([document])
	clf.partial_fit(X, [y])

def db_entry(true_result, document):
	"""
	將資料存入sqlite資料庫當中
	"""
	add_data = resultData(document=document, result=true_result, createDate=datetime.now())
	db.session.add(add_data)
	db.session.commit()

class ReviewForm(Form):
	"""
	建立表單，使得request.form有spanclassifier的method
	"""
	spanclassifier = TextAreaField('', [validators.DataRequired(), validators.length(min=15)]) # validators.DataRequired()為必須含有資料

"""
web browser -> request -> web server -> request -> flask
decorator用來指定應該觸發home函數執行的url
@app.route('/') 為路徑修飾器，當遇到這個url時，會觸發route這個函數
"""
@app.route('/', methods=['GET']) # 主頁面
def home():
	"""
	request.form來訪問表單數據，post提交的數據，有出現的就可以使用在html的name裡面
	"""
	form = ReviewForm(request.form) # 建立起表達，確認使否符合格式 並納入request.form的其中一個method裡
	return render_template('home.html', form=form)

"""
使用post方法將表單數據中的用戶輸入訊息傳送給server
"""
@app.route('/predict', methods=['POST'])
def results():
	# 得到post而來的資料
	form = ReviewForm(request.form)
	if request.method == 'POST':
		message = request.form['spanclassifier']
		result, y, proba = predict(message)
		return render_template('result.html', content=message, prediction=result, probability=round(proba*100, 2))
	return render_template('home.html', form=form)

@app.route('/thanks', methods=['POST'])
def feedback():
	"""
	有在result.html的form表單中的name使用 得到來自result.html傳來的request.form
	"""
	feedback = request.form['feedback_button']
	review = request.form['review']
	prediction = request.form['prediction']

	inv_label = {'not spam': 0, 'spam': 1}
	y = inv_label[prediction]
	if feedback == 'Incorrect':
		y = int(not(y))
	train(review, y)
	db_entry(prediction, review)
	return render_template('thanks.html')

class apiPredict(Resource):
	"""
	建立api返回predict的結果
	"""
	def post(self):
		postedData = request.get_json()

		x = postedData['Document']
		result, y, proba = predict(x)
		retJson = {
			'data': x,
			'result_proba': '{}: {}'.format(result, proba)
		}

		db_entry(result, x)
		return jsonify(retJson)

api.add_resource(apiPredict, '/api/predict')

"""
__name__ == '__main__' 確保直接執行script才啟動web server、
在app.run中設置debug=True進而激活了flask的調試器
run在服務器上運行程序
"""
if __name__ == '__main__':
	app.run(host='0.0.0.0')

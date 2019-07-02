"""
將由python解釋器執行已運行flask web應用程式的主要代碼
針對消息進行分類
"""

# render_template讓flask可以渲染於網路瀏覽器中
from flask import Flask, render_template, url_for, request
# Form形成表單， TextAreaField建立填空欄， validators 驗證表單內容是否符合格式
from wtforms import Form, TextAreaField, validators 
import os
import pandas as pd
import numpy as np
import sqlite3
import pickle
from update import update_model

"""
使用__name__可以讓flask知道它可以在同一個目錄底下，找到html模板的文件夾
"""
app = Flask(__name__)

# 準備model
cur_dir = os.path.dirname(__file__)
clf = pickle.load(open(os.path.join(cur_dir, 'pickle_model/classifier.pkl'), 'rb'))
cv = pickle.load(open(os.path.join(cur_dir, 'pickle_model/countvectorizer.pkl'), 'rb'))
db = os.path.join(cur_dir, 'spam_classification.sqlite')

def predict(document):
	label = {0: 'not spam', 1: 'spam'}
	X = cv.transform([document])
	y = clf.predict(X)
	proba = np.max(clf.predict_proba(X))
	return label[int(y)], y, proba

def train(document, y):
	X = cv.transform([document])
	clf.partial_fit(X, [y])

def sqlite_entry(path, document, y):
	conn = sqlite3.connect(path)
	c = conn.cursor()
	c.execute('INSERT INTO spam_db (message, label) VALUES (?, ?)', (document, y))
	conn.commit()
	conn.close()


class ReviewForm(Form):
	spanclassifier = TextAreaField('', [validators.DataRequired(), validators.length(min=15)])

"""
decorator用來指定應該觸發home函數執行的url
@app.route('/') 為路徑修飾器，當遇到這個url時，會觸發route這個函數
"""
@app.route('/') # 主頁面
def home():
	form = ReviewForm(request.form)
	return render_template('home.html', form=form)

"""
使用post方法將表單數據中的用戶輸入訊息傳送給server
"""
@app.route('/predict', methods=['POST'])
def results():
	form = ReviewForm(request.form)
	if request.method == 'POST':
		message = request.form['spanclassifier']
		result, y, proba = predict(message)
		return render_template('result.html', content=message, prediction=result, probability=round(proba*100, 2))
	return render_template('home.html', form=form)

@app.route('/thanks', methods=['POST'])
def feedback():
	feedback = request.form['feedback_button']
	review = request.form['review']
	prediction = request.form['prediction']

	inv_label = {'not spam': 0, 'spam': 1}
	y = inv_label[prediction]
	if feedback == 'Incorrect':
		y = int(not(y))
	train(review, y)
	sqlite_entry(db, review, y)
	return render_template('thanks.html')

"""
在app.run中設置debug=True進而激活了flask的調試器
run在服務器上運行程序
"""
if __name__ == '__main__':
	app.run(debug=True)

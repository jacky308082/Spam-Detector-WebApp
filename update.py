import pickle
import sqlite3
import numpy as np
import os

def update_model(db_path, model):

	conn = sqlite3.connect(db_path)
	c = conn.cursor()
	c.execute('SELECT * FROM spam_db')

	results = c.fetchone()
	data = np.array(results)
	X = data[1]
	y = data[2].astype(int)

	classes = np.array([0, 1])
	X_train = cv.transform([X])
	clf.partial_fit(X_train, [y], classes=classes)

cur_dir = os.path.dirname(__file__)

clf = pickle.load(open(os.path.join(cur_dir, 'pickle_model/classifier.pkl'), 'rb'))
cv = pickle.load(open(os.path.join(cur_dir, 'pickle_model/countvectorizer.pkl'), 'rb'))

db = os.path.join(cur_dir, 'spam_classification.sqlite')

update_model(db_path=db, model=clf)
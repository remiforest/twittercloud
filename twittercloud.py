#! /usr/bin/python

import logging
import json
import twitter
import os
from flask import Flask, render_template, request
from maprutils import open_db, open_table
from maprdb.conditions import Condition


import datetime


# logging.basicConfig(filename='logs/twittercloud.log',level=logging.DEBUG)

# Retrieves current cluster name
with open('/opt/mapr/conf/mapr-clusters.conf', 'r') as f:
    first_line = f.readline()
    cluster_name = first_line.split(' ')[0]
    logging.debug('Cluster name : {}'.format(cluster_name))


home_dir = "/mapr/" + cluster_name + "/twittercloud/"

if not os.path.isdir(home_dir):
    os.system("mkdir -p " + home_dir)

TWEETS_TABLE = home_dir + "tweets"
KEYWORDS_TABLE = home_dir + "keywords"


condition = {"keyword": "kubernetes"}
# c = Condition({"keyword": {"$eq": "kubernetes"}})
# c = Condition()._is("keyword", Op.EQUAL, 'kubernetes')
# print(c)
# words = []
db = open_db()
tt = open_table(db, TWEETS_TABLE)

condition1 = Condition([{ "some_date": datetime.datetime(2019, 9, 10, 12, 21, 35)}, {"some_float": {"$gt": 0}}])
result1 = [x for x in tt.find_by_condition(condition1, columns=['some_date', 'some_number'])]
print(result1)
# for tweet in tt.find_by_condition(c):
# for tweet in tt.find(condition):
#   print(tweet)

# app = Flask(__name__)


@app.route('/')
def home():
  return render_template('twittercloud.html')

@app.route('/get_keywords',methods=['GET'])
def get_keywords():
  keywords = []
  db = open_db()
  kt = open_table(db, KEYWORDS_TABLE)
  for kw in kt.find():
    keywords.append(kw)
  return json.dumps(keywords)

@app.route('/get_words',methods=['POST'])
def get_words():
  keyword = request.form['keyword']
  print(keyword)
  condition = {"keyword": keyword}
  c = Condition(condition)
  c = Condition({"keyword": {"$eq": "kubernetes"}})
  c = Condition()._is("keyword", Op.EQUAL, 'kubernetes')
  print(c)
  words = []
  db = open_db()
  tt = open_table(db, TWEETS_TABLE)
  for tweet in tt.find_by_condition(c):
  # for tweet in tt.find(columns=['text']):
    # text = tweet["text"]
    print(tweet)
    # for w in text.split():
    #   words.append(w)
  return json.dumps(words)

app.run(debug=True,host='0.0.0.0',port=80)


#! /usr/bin/python3

import os
import json
import argparse
import logging
import maprdb
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from auth import TwitterAuth
from maprutils import open_db, open_table

logging.basicConfig(filename='logs/scanner.log',level=logging.DEBUG)


# Retrieves current cluster name
with open('/opt/mapr/conf/mapr-clusters.conf', 'r') as f:
    first_line = f.readline()
    cluster_name = first_line.split(' ')[0]
    logging.debug('Cluster name : {}'.format(cluster_name))



parser = argparse.ArgumentParser(description='Scan twitter for the keyword and store in table')
parser.add_argument('--keyword',help='keyword to scan',default="MapR",required=True)
args = parser.parse_args()

keyword = args.keyword

home_dir = "/mapr/" + cluster_name + "/twittercloud/"

if not os.path.isdir(home_dir):
    os.system("mkdir -p " + home_dir)

TWEETS_TABLE = home_dir + "tweets"
KEYWORDS_TABLE = home_dir + "keywords"

db = open_db()
tweets = open_table(db, TWEETS_TABLE)
keywords = open_table(db, KEYWORDS_TABLE)


class StdOutListener(StreamListener):
  
  def on_data(self, data):
    tweet = json.loads(data)
    _id = str(tweet["id"])
    text = tweet["text"]
    print(text)
    # Insert tweet in tweets table
    tweets.insert_or_replace(maprdb.Document({"_id":_id,"keyword":keyword,"text":text}))
    tweets.flush()
    
    # Update count for keyword
    try:
      keyword_count = keywords.find_by_id(keyword)["count"]
    except:
      keyword_count = 0
    keyword_count += 1
    count_doc = {"_id":keyword,"count":keyword_count}
    keywords.insert_or_replace(maprdb.Document(count_doc))
    keywords.flush()


  def on_error(self, status):
    print("ERROR")
    print(status)



try:
  #Create the listener
  l = StdOutListener()
  auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
  auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)

  #Connect to the Twitter stream
  stream = Stream(auth, l)  

  #Terms to track
  stream.filter(track=[keyword])


except KeyboardInterrupt:
  #User pressed ctrl+c -- get ready to exit the program
  pass

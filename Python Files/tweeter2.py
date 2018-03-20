import tweepy
import numpy as np
import pandas as pd
import datetime
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import date, timedelta
import nltk
####input your credentials here
consumer_key = 'AYDNqr9ycBI9qaOWoYXJgYnKY'
consumer_secret = 'tSHVPOr6JrQ9KNnqX1aSOGnKecmPeQQ37j81JAURI0t6deb8AA'
access_token = '2493864625-SSCalZj2of8hITNgrv4gMvNZX7seGTSWD2MQI0H'
access_token_secret = '5JBwqg2jWjijXgIRpEsdLrGRYWEuNmc4M0ibfRL2xzrhd'
# f = open('C:/Users/anshul/jupyter/sample.txt', 'r+')
# f.truncate()
hashtagtweet=input("Enter the hash tag tweet: ")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
#####United Airlines
nltk.download('vader_lexicon')

now=datetime.datetime.now()
enddate=now.date()
startdate=enddate - timedelta(10)

for i, tweet in enumerate(tweepy.Cursor(api.search,q=hashtagtweet,count=100,
                           lang="en",
                           since=startdate, until=enddate).items()):
    # file = open('C:/Users/anshul/jupyter/sample.txt', 'a')
    # pos, neg=senti_classifier.polarity_scores(tweet.text)
    # print (tweet.created_at, tweet.text)
    pos=0
    neg=0
    neu=0

    sentence = tweet.text
    sid=SentimentIntensityAnalyzer()
    #sentence = sentence.replace('RT @', '')
    sentence = re.sub('[^ a-zA-Z0-9' ']', '', sentence)
    dic = {}
    print(i, tweet)
	# dic.update()


    sentence = sentence.lower()
    sentence1=[tweet.text]
    for s in sentence1:
        ss = sid.polarity_scores(s)
        pos=pos+ss['pos']
        neg=neg+ss['neg']
        neu=neu+ss['neu']
    if pos>neg :
        d='Positive'
    elif pos<neg :
        d='Negative'
    else:
        d='Neutral'
    # file.write(': ' + str(d))
    # file.write('\n')
    print (d)
    #time.sleep(1)
    # file.close()


from flask import Flask, render_template, request
import tweepy
import numpy as np
import pandas as pd
import datetime
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import date, timedelta   
import nltk
import time


def search(query, max_items):
    consumer_key = 'AYDNqr9ycBI9qaOWoYXJgYnKY'
    consumer_secret = 'tSHVPOr6JrQ9KNnqX1aSOGnKecmPeQQ37j81JAURI0t6deb8AA'
    access_token = '2493864625-SSCalZj2of8hITNgrv4gMvNZX7seGTSWD2MQI0H'
    access_token_secret = '5JBwqg2jWjijXgIRpEsdLrGRYWEuNmc4M0ibfRL2xzrhd'

    hashtagtweet = query
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    nltk.download('vader_lexicon')

    now = datetime.datetime.now()
    enddate = now.date()
    startdate = enddate - timedelta(10)
    lis = []
    counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

    for i, tweet in enumerate(tweepy.Cursor(api.search, q=hashtagtweet, count=100,lang="en",since=startdate, until=enddate).items(max_items)):
        pos = 0
        neg = 0
        neu = 0

        sentence = tweet.text
        date = tweet.created_at.strftime('%d %b %Y')
        user = tweet.user
        username = user.screen_name
        link = 'https://twitter.com/' + username

        sid = SentimentIntensityAnalyzer()
        sentence = re.sub('[^ a-zA-Z0-9' ']', '', sentence)
        sentence = sentence.lower()
        sentence1 = [tweet.text]
        for s in sentence1:
            ss = sid.polarity_scores(s)
            pos = pos + ss['pos']
            neg = neg + ss['neg']
            neu = neu + ss['neu']
        if pos > neg:
            d = 'Positive'
            counts['Positive'] += 1
        elif pos < neg:
             d = 'Negative'
             counts['Negative'] += 1
        else:
            d = 'Neutral'
            counts['Neutral'] += 1

        lis.append({'id': i, 'username': username, 'link': link, 'text': sentence, 'date': date, 'inference': d})
    return lis, counts


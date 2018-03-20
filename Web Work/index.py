from flask import Flask, render_template, request
import tweepy
import numpy as np
import pandas as pd
from datetime import datetime , timedelta
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import date, timedelta
import nltk
from tweeter2 import search
from similar_names import get_names

app = Flask(__name__)

def getText():
    with open('static/dynamic.txt') as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/main")
def main_page():
    query = request.args.get('query')
    max_items = 100  # request.args.get('max_items')

    final_list = []
    final_count = []

    consumer_key = 'AYDNqr9ycBI9qaOWoYXJgYnKY'
    consumer_secret = 'tSHVPOr6JrQ9KNnqX1aSOGnKecmPeQQ37j81JAURI0t6deb8AA'
    access_token = '2493864625-SSCalZj2of8hITNgrv4gMvNZX7seGTSWD2MQI0H'
    access_token_secret = '5JBwqg2jWjijXgIRpEsdLrGRYWEuNmc4M0ibfRL2xzrhd'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    nltk.download('vader_lexicon')

    for i in range(10):
        N = 10 - i
        date_start = datetime.now() - timedelta(days=N)
        date_until = datetime.now() - timedelta(days=N - 2)

        lis, counts = search(api, 'modi', 100, date_start, date_until)
        print(counts)

        final_list.append(lis)
        final_count.append(counts)



    print(lis, counts)
    data = {'tweets': lis}


    

    return render_template('main.html', data=data)

@app.route('/compare')
def comapre_page():
    return render_template('compare.html')

if __name__ == '__main__':
    app.run(debug=True)

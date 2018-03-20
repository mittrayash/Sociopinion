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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

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

    #nltk.download('vader_lexicon')

    for i in range(10):
        N = 10 - i
        date_start = datetime.now() - timedelta(days=N)
        date_until = datetime.now() - timedelta(days=N - 2)

        lis, counts = search(api, query, 23, date_start, date_until)
        print(counts)

        final_list.append(lis)
        final_count.append(counts)

    for i in range(len(final_count)):
        temp_list = [final_count[i]['Positive'] , final_count[i]['Neutral'] , final_count[i]['Negative']]
        final_count[i] = temp_list

    pos_line_graph_list = []
    neu_line_graph_list = []
    neg_line_graph_list = []

    for i in range(len(final_count)):
        pos_line_graph_list.append(final_count[i][0])
        neu_line_graph_list.append(final_count[i][1])
        neg_line_graph_list.append(final_count[i][2])

    total_pos = 0
    total_neu = 0
    total_neg = 0
    avg_pos = 0
    avg_neu = 0
    avg_neg = 0

    for i in range(len(final_count)):
        total_pos += final_count[i][0]
        total_neu += final_count[i][1]
        total_neg += final_count[i][2]

    avg_pos = total_pos/(total_pos + total_neg)
    avg_neg = total_neg/(total_pos + total_neg)

    data = {'tweets': final_list , 'pos_line_data' : pos_line_graph_list
            , 'neu_line_data' : neu_line_graph_list , 'neg_line_data' : neg_line_graph_list
            , 'total_pos' : total_pos , 'total_neu' : total_neu
            ,'total_neg' : total_neg ,'avg_pos' : avg_pos
            , 'avg_neg' : avg_neg}

    print(data)

    return render_template('main.html', data=data)

@app.route('/compare')
def compare_page():
    return render_template('compare.html')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify, session
import tweepy
import numpy as np
import pandas as pd
from datetime import datetime , timedelta
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import date, timedelta
import nltk
from tweeter2 import search
import json
from similar_names import get_names

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/main")
def main_page():
    query = request.args.get('query')
    max_items = 50  # request.args.get('max_items')

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
    dates = []

    for i in range(10):
        N = 10 - i
        date_start = datetime.now() - timedelta(days=N)
        date_now = datetime.now() - timedelta(days=N - 1)
        date_until = datetime.now() - timedelta(days=N - 2)

        dates.append(date_now.strftime('%d %b'))

        lis, counts = search(api, query, max_items, date_start, date_until)
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
            , 'avg_neg' : avg_neg ,  'name' : query , 'dates' : dates}

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    print(lis, counts)
    similar = get_names(query)

    return render_template('main.html', data=data, similar=similar)

@app.route('/compare')
def compare_page():

    with open('data.json' , 'r') as data_file:
        data1 = json.load(data_file)

    btn = request.args.get('btn')
    comp_data = request.args.get('comp_data')

    query = ''

    if (btn):
        query = btn
    else:
        query = comp_data

    max_items = 50  # request.args.get('max_items')

    final_list = []
    final_count = []

    consumer_key = 'AYDNqr9ycBI9qaOWoYXJgYnKY'
    consumer_secret = 'tSHVPOr6JrQ9KNnqX1aSOGnKecmPeQQ37j81JAURI0t6deb8AA'
    access_token = '2493864625-SSCalZj2of8hITNgrv4gMvNZX7seGTSWD2MQI0H'
    access_token_secret = '5JBwqg2jWjijXgIRpEsdLrGRYWEuNmc4M0ibfRL2xzrhd'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # nltk.download('vader_lexicon')
    dates = []
    for i in range(10):
        N = 10 - i
        date_start = datetime.now() - timedelta(days=N)
        date_now = datetime.now() - timedelta(days=N-1)

        dates.append(date_now.strftime('%d %b'))

        date_until = datetime.now() - timedelta(days=N - 2)

        lis, counts = search(api, query, max_items, date_start, date_until)
        print(counts)

        final_list.append(lis)
        final_count.append(counts)

    for i in range(len(final_count)):
        temp_list = [final_count[i]['Positive'], final_count[i]['Neutral'], final_count[i]['Negative']]
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
    avg_neg = 0

    for i in range(len(final_count)):
        total_pos += final_count[i][0]
        total_neu += final_count[i][1]
        total_neg += final_count[i][2]

    avg_pos = total_pos / (total_pos + total_neg)
    avg_neg = total_neg / (total_pos + total_neg)

    data2 = {'tweets': final_list, 'pos_line_data': pos_line_graph_list
        , 'neu_line_data': neu_line_graph_list, 'neg_line_data': neg_line_graph_list
        , 'total_pos': total_pos, 'total_neu': total_neu
        , 'total_neg': total_neg, 'avg_pos': avg_pos
        , 'avg_neg': avg_neg , 'name' : query , 'dates' : dates}

    final_data = {'data1' : data1 , 'data2' : data2}

    return render_template('compare.html' , final_data=final_data)

if __name__ == '__main__':
    app.run(debug=True)

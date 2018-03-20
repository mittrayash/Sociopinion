from flask import Flask, render_template, request
import tweepy
import numpy as np
import pandas as pd
import datetime
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import date, timedelta
import nltk
from tweeter2 import search

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
    
    if not query.startswith('ajax-'):
        lis = search(query, 10)
        print('Normal')
        data = {'tweets': lis}
        return render_template('main.html', data=data)
    else:
        print('ajax')
        temp = query[5:]
        print(temp)
        lis = search(temp, 10)
        data = {'tweets': lis}
        return data

@app.route('/compare')
def comapre_page():
    return render_template('compare.html')

if __name__ == '__main__':
    app.run(debug=True)

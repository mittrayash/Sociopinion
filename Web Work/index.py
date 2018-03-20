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
    lis, counts = search(query, 100)
    print(lis, counts)
    data = {'tweets': lis}
    return render_template('main.html', data=data)

@app.route('/compare')
def comapre_page():
    return render_template('compare.html')

if __name__ == '__main__':
    app.run(debug=True)

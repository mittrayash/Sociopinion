import tweepy
import re
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import nltk
from textblob import TextBlob

def search(api, query, max_items, startdate, enddate):
    lis = []
    counts = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

    start_date = startdate.strftime('%Y-%m-%d')
    end_date = enddate.strftime('%Y-%m-%d')

    for i, tweet in enumerate(
            tweepy.Cursor(api.search, q=query, count=100, lang="en", since=start_date, until=end_date).items(max_items)):
        pos = 0
        neg = 0
        neu = 0

        sentence = tweet.text
        date = tweet.created_at.strftime('%d %b %Y')
        user = tweet.user
        username = user.screen_name
        link = 'https://twitter.com/' + username

        # sid = SentimentIntensityAnalyzer()
##############################################
        sentence = sentence.replace('"', "'")
        sentence = re.sub('[^ a-zA-Z0-9,.()!@#$%^&*_+-=~`<>?/\|{}:\']', '', sentence)


        # sentence = sentence.lower()
        # sentence1 = [tweet.text]

        test = TextBlob(sentence)
        pol = test.sentiment.polarity

        if pol > 0.0:
            d = 'Positive'
            counts['Positive'] += 1
        elif pol < 0.0:
            d = 'Negative'
            counts['Negative'] += 1
        else:
            d = 'Neutral'
            counts['Neutral'] += 1

        lis.append({'id': i, 'username': username, 'link': link, 'text': sentence, 'date': date, 'inference': d})
    return lis, counts

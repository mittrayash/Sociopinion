from flask import Flask, render_template, request, url_for
import tweepy
from datetime import datetime
from datetime import timedelta
# import nltk
from tweeter2 import search
from similar_names import get_names

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

@app.route("/")
def hello():
    return render_template('index.html')

max_items = 20

@app.route("/feedback", methods=['POST'])
def feedback():
    date = datetime.now()
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    file = open('feedback.csv', 'a')
    file.write(name + ',' + email + ',' + message + ',' + str(date) + '\n')
    return render_template('feedback.html')

@app.route("/main")
def main_page():
    try:
        global max_items
        query = request.args.get('query')
        # request.args.get('max_items')

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
            date_now = datetime.now() - timedelta(days=N - 1)
            date_until = datetime.now() - timedelta(days=N - 2)

            dates.append(date_now.strftime('%d %b'))

            lis, counts = search(api, query, max_items, date_start, date_until)
            print("Completed {} of 10".format(i+1))
            final_list.append(lis)
            final_count.append(counts)

        for i in range(len(final_count)):
            temp_list = [final_count[i]['Positive'] , final_count[i]['Neutral'] , final_count[i]['Negative']]
            final_count[i] = temp_list

        pos_line_graph_list = []
        neu_line_graph_list = []
        neg_line_graph_list = []

        total_pos = 0
        total_neu = 0
        total_neg = 0

        for i in range(len(final_count)):
            pos_line_graph_list.append(final_count[i][0])
            neu_line_graph_list.append(final_count[i][1])
            neg_line_graph_list.append(final_count[i][2])

            total_pos += final_count[i][0]
            total_neu += final_count[i][1]
            total_neg += final_count[i][2]

        avg_pos = total_pos/(total_pos + total_neg)
        avg_neg = total_neg/(total_pos + total_neg)

        data = {'tweets': final_list , 'pos_line_data' : pos_line_graph_list
                , 'neu_line_data' : neu_line_graph_list , 'neg_line_data' : neg_line_graph_list
                , 'total_pos' : total_pos , 'total_neu' : total_neu
                , 'total_neg' : total_neg ,'avg_pos' : avg_pos
                , 'avg_neg' : avg_neg ,  'name' : query , 'dates' : dates}

        similar = get_names(query)

        return render_template('main.html', data=data, similar=similar)
    except ZeroDivisionError:
        return render_template('error.html')

@app.route('/compare')
def compare_page():
    global max_items

    btn = request.args.get('btn')
    comp_data = request.args.get('comp_data')

    if btn:
        query = btn
    else:
        query = comp_data

    # request.args.get('max_items')

    final_list = []
    final_count = []

    consumer_key = 'AYDNqr9ycBI9qaOWoYXJgYnKY'
    consumer_secret = 'tSHVPOr6JrQ9KNnqX1aSOGnKecmPeQQ37j81JAURI0t6deb8AA'
    access_token = '2493864625-SSCalZj2of8hITNgrv4gMvNZX7seGTSWD2MQI0H'
    access_token_secret = '5JBwqg2jWjijXgIRpEsdLrGRYWEuNmc4M0ibfRL2xzrhd'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    dates = []
    for i in range(10):
        N = 10 - i
        date_start = datetime.now() - timedelta(days=N)
        date_now = datetime.now() - timedelta(days=N-1)

        dates.append(date_now.strftime('%d %b'))

        date_until = datetime.now() - timedelta(days=N - 2)

        lis, counts = search(api, query, max_items, date_start, date_until)

        final_list.append(lis)
        final_count.append(counts)

    for i in range(len(final_count)):
        temp_list = [final_count[i]['Positive'], final_count[i]['Neutral'], final_count[i]['Negative']]
        final_count[i] = temp_list

    pos_line_graph_list = []
    neu_line_graph_list = []
    neg_line_graph_list = []

    total_pos = 0
    total_neu = 0
    total_neg = 0

    for i in range(len(final_count)):
        pos_line_graph_list.append(final_count[i][0])
        neu_line_graph_list.append(final_count[i][1])
        neg_line_graph_list.append(final_count[i][2])

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

    final_data = {'data2': data2}

    return render_template('compare.html', final_data=final_data)


if __name__ == '__main__':
    app.run(debug=True)

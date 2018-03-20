from flask import Flask, render_template, request

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
    tweets = getText()
    data = {'tweets' : tweets}
    get_data = request.args.get('query')
    return render_template('main.html' , data=data)

@app.route('/compare')
def comapre_page():
    return render_template('compare.html')

if __name__ == '__main__':
    app.run(debug=True)

# Team50 - Yuanyi Zhang - 1206297
from flask import Flask,render_template
import json
app = Flask(__name__)

f = open('final.json')
content = json.load(f)


@app.route('/')
def homepage():
    # return content
    return render_template("index.html",content=content['features'])

if __name__=='__main__':
    app.run(host='0.0.0.0')


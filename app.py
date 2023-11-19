from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from search import Search
import json

app = Flask(__name__)

@app.route("/",methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/search",methods=['GET','POST'])
def search():
    if request.method == "POST":
        text = request.form.get('text')
        print(text)
        S = Search(text) 
        dic = S.search_papers()
        S.print_papers(dic)
        return redirect('/result')
    else:
        return render_template('search.html')
@app.route("/result",methods = ['GET', 'POST'])
def result():
    if request.method == "GET":
        dir = "result.json"
        encoding = "utf-8"	# 読み込むファイルのエンコードによって適宜変える。
        with open(dir, mode="rt", encoding="utf-8") as f:
            dic = json.load(f)		# JSONのファイル内容をdictに変換する。
        posts = dic["data"]
        return render_template('result.html',posts = posts)
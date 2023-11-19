from flask import Flask
from flask import render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
from search import Search
import json
from citation import Citation
from reference import Reference

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
        dir = "results.json"
        encoding = "utf-8"	# 読み込むファイルのエンコードによって適宜変える。
        with open(dir, mode="rt", encoding="utf-8") as f:
            dic = json.load(f)		# JSONのファイル内容をdictに変換する。
        posts = dic["data"]
        return render_template('result.html',posts = posts)

@app.route("/result/<paperId>/citation",methods = ['GET', 'POST'])
def citation(paperId):
    if request.method == "GET":
        S = Citation(paperId) 
        dic = S.search_citing_papers()
        S.print_citing_papers(dic)
        dir = "citations.json"
        encoding = "utf-8"	# 読み込むファイルのエンコードによって適宜変える。
        with open(dir, mode="rt", encoding="utf-8") as f:
            dic = json.load(f)		# JSONのファイル内容をdictに変換する。
        data = dic["data"]
        posts = [d['citingPaper'] for d in data]
        return render_template('result.html',posts = posts)
    else:
        return render_template('search.html')

@app.route("/result/<paperId>/reference",methods = ['GET', 'POST'])
def reference(paperId):
    if request.method == "GET":
        S = Reference(paperId) 
        dic = S.search_refer_papers()
        S.print_refer_papers(dic)
        dir = "references.json"
        encoding = "utf-8"	# 読み込むファイルのエンコードによって適宜変える。
        with open(dir, mode="rt", encoding="utf-8") as f:
            dic = json.load(f)		# JSONのファイル内容をdictに変換する。
        data = dic["data"]
        posts = [d['citedPaper'] for d in data]
        return render_template('result.html',posts = posts)
    else:
        return render_template('search.html')
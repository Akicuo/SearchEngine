from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
from datetime import datetime
from requests import get, post
from outside_model.om import SearchAgentEngine
import os


app = Flask(__name__)
app.secret_key = "2024-BLJ-Projekt" # This ofcourse is different in the real web app

SAE = SearchAgentEngine(API_Key='LAYLAN-01i2mdabdj3929dk2lem2l2cd1f4762e84d')





@app.route('/', methods=['GET'])
def index():
    user = session.get("user")
    return render_template('index.html', current_user=user, isProUser=False)

@app.route('/login', methods=['GET']) # Login or Register Page
def login():
    user = session.get("user")
    return render_template('index.html', user=user)

@app.route('/register', methods=['GET']) # Login or Register Page
def register():
    user = session.get("user")
    return render_template('index.html', user=user)

@app.route('/history', methods=['GET'])
def history():
    user = session.get("user")
    return render_template('index.html', user=user)

@app.route('/home', methods=['GET'])
def home():
    user = session.get("user")
    return render_template('index.html', user=user)


@app.route('/about', methods=['GET'])
def about():
    user = session.get("user")
    return render_template('index.html', user=user)

@app.route('/contact', methods=['GET'])
def contact():
    user = session.get("user")
    return render_template('index.html', user=user)

@app.route('/profile', methods=['GET'])
def profile():
    user = session.get("user")
    return render_template('index.html', user=user)


@app.route('/search', methods=['GET'])
def search():
    user = session.get("user")
    seach_results = SAE.Search(request.get_data["query"])
    return render_template('index.html', apiKey=SAE.KeyIsUsable(), results=seach_results, user=user)



@app.route('/searches')
def searches():
    self_searches = session.get("self_searched", [])
    return render_template('search_stats.html', self_searches=self_searches)


@app.route('/client-api/search', methods=['POST'])
def clientsearch():
    return SAE.Search(request.args.get("q"))



if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True, port=5000)
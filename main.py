from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
from datetime import datetime
from requests import get, post
from outside_model.om import SearchAgentEngine
import os


app = Flask(__name__).secret_key = "2024-BLJ-Projekt" 



SAE = SearchAgentEngine(API_Key='LAYLAN-01i2mdabdj3929dk2lem2l2cd1f4762e84d')

"""
ses_h           | session_history| LIST   | List of all the searches the user has done during the session
ser_h           | server_history| LIST   | List of all the searches the user has done during all sessions which are saved on the server
current_user    | current_user  | CLASS -> is_authenticated (BOOL) | Is a class containing variables for the user
"""

class current_user:
    is_authenticated:bool
    isProUser:bool
    isGuest:bool
    img_link:str
    username:str





@app.route('/', methods=['GET'])
def index():
    user = session.get("user")
    is_logged_in = session.get("ili")
    return render_template('index.html', current_user=current_user, isProUser=current_user.is)

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
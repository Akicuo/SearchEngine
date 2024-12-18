from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
from datetime import datetime
from requests import get, post
from outside_model.om import SearchAgentEngine
import os
import outside_model.sql_model as sql_model


app = Flask(__name__)
app.secret_key = "2024-BLJ-Projekt" 



SAE = SearchAgentEngine(API_Key='LAYLAN-01i2mdabdj3929dk2lem2l2cd1f4762e84d')
default_pfp = 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/768px-Default_pfp.svg.png'
connection = sql_model.Connector()

class UserProfile:
    def __init__(self, is_authenticated=False, isProUser=False, isGuest=False, img_link=default_pfp, username="Guest", id:int=0):
        self.is_authenticated = is_authenticated
        self.isProUser = isProUser
        self.isGuest = isGuest
        self.img_link = img_link
        self.username = username
        self.id = id
    def FindOutSubscriptionType(self):
        global connection
        cursor = connection.cursor()
        cursor.execute("SELECT subscription FROM users WHERE id = %s", (self.id,))
        subscription = cursor.fetchone()
        if subscription[0] == 'free':

            return 'Free'
        elif subscription[0] == 'premium':
            return 'Premium'
    def FindOutUsername(self) -> str:
        global connection
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users WHERE id = %s", (self.id,))
        name = cursor.fetchone()
        return name[0]
    def FindOutProfileIMG(self) -> str:
        global connection
        cursor = connection.cursor()
        cursor.execute("SELECT profile_img FROM users WHERE id = %s", (self.id,))
        pfp = cursor.fetchone()
        return pfp[0]
    
    
        

c_user = UserProfile()

"""
SESSION VAR    |   SESSION TYPE     |       DESCRIBE

----------------|-------------------|-------------------
user         |   string        |   0/1;USERNAME;img;0/1
"""

@app.route('/', methods=['GET'])
def index():
    user = session.get("id")
    if user is not None:
            c_user.is_authenticated=True
            c_user.username=c_user.FindOutUsername()
            c_user.img_link=c_user.FindOutProfileIMG()
            c_user.isProUser=c_user.FindOutSubscriptionType()
            
    return render_template('index.html', current_user=c_user, isProUser=c_user.isProUser)

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
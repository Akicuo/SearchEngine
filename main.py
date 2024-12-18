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
connection = sql_model.Connector(host="mysql2.webland.ch", user="d041e_seai", password="seaiSEAI$2024", db="d041e_seai").connect()

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
    user = session.get("id")
    return render_template('index.html', user=user)

@app.route('/register', methods=['GET']) # Login or Register Page
def register():
    user = session.get("user")
    return render_template('index.html', user=user)

@app.route('/history', methods=['GET'])
def history():
    user = session.get("user")
    return render_template('index.html', user=user)




@app.route('/about', methods=['GET'])
def about():
    user = session.get("id")
    if user is not None:
            c_user.is_authenticated=True
            c_user.username=c_user.FindOutUsername()
            c_user.img_link=c_user.FindOutProfileIMG()
            c_user.isProUser=c_user.FindOutSubscriptionType()
    return render_template('index.html', user=user)

@app.route('/contact', methods=['GET'])
def contact():
    user = session.get("id")
    if user is not None:
            c_user.is_authenticated=True
            c_user.username=c_user.FindOutUsername()
            c_user.img_link=c_user.FindOutProfileIMG()
            c_user.isProUser=c_user.FindOutSubscriptionType()
    return render_template('index.html', user=user)

@app.route('/profile', methods=['GET'])
def profile():
    user = session.get("id")
    if user is not None:
            c_user.is_authenticated=True
            c_user.username=c_user.FindOutUsername()
            c_user.img_link=c_user.FindOutProfileIMG()
            c_user.isProUser=c_user.FindOutSubscriptionType()
    return render_template('index.html', user=user)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get("q")
    user = session.get("id")
    if user is not None:
        c_user.is_authenticated = True
        c_user.username = c_user.FindOutUsername()
        c_user.img_link = c_user.FindOutProfileIMG()
        c_user.isProUser = c_user.FindOutSubscriptionType()
    
    search_results = SAE.Search(query=query)   
    return render_template('search.html', 
                           results=search_results, 
                           current_user=c_user, 
                           search_query=query,
                           isProUser=c_user.isProUser)



@app.route('/searches')
def searches():
    user = session.get("id")
    if user is not None:
            c_user.is_authenticated=True
            c_user.username=c_user.FindOutUsername()
            c_user.img_link=c_user.FindOutProfileIMG()
            c_user.isProUser=c_user.FindOutSubscriptionType()
    self_searches = session.get("self_searched", [])
    return render_template('search_stats.html', self_searches=self_searches)





if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True, port=5000)
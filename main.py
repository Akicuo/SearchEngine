from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash,
)
import json
from datetime import datetime
from requests import get, post
from outside_model.om import SearchAgentEngine
import os
import outside_model.sql_model as sql_model
import hashlib

app = Flask(__name__)
app.secret_key = "2024-BLJ-Projekt"

SAE = SearchAgentEngine(API_Key="LAYLAN-01i2mdabdj3929dk2lem2l2cd1f4762e84d")
default_pfp = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/768px-Default_pfp.svg.png"
connection = sql_model.Connector(
    host="mysql2.webland.ch",
    user="d041e_seai",
    password="seaiSEAI$2024",
    db="d041e_seai",
).connect()

def FindOutSubscriptionType(id):
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT subscription FROM users WHERE id = %s", (id,))
    subscription = cursor.fetchone()
    if subscription == "free":
        return "Free"
    elif subscription == "premium" or subscription == None:
        return "Premium"

def FindOutUsername(id) -> str:
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM users WHERE id = %s", (id,))
    name = cursor.fetchone()
    return name if name else None

def FindOutProfileIMG(id) -> str:
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT img FROM users WHERE id = %s", (id,))
    pfp = cursor.fetchone()
    return pfp if pfp else default_pfp
def FindOutTimeAfterCreation(id):
    """
    Find out how long the user has been created for
    """
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT creation_date FROM users WHERE id = %s", (id,))
    created_at = cursor.fetchone()
    
    if created_at:

        if isinstance(created_at, tuple):
            created_at = created_at[0]
        

        if not isinstance(created_at, datetime):
            try:

                created_at = datetime.strptime(str(created_at), "%Y-%m-%d %H:%M:%S")
            except Exception as e:
                print(f"Error converting creation date: {e}")
                return "Unknown"
        
   
        time_diff = datetime.now() - created_at
        days = time_diff.days
        
        return days
    else:
        return "Unknown"




def id_valid(session_id):   
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM users WHERE id = %s", (session_id,))
    p = cursor.fetchone()
    if p is not None:
        return True
    else:
        return False
def add_to_searches(session_id, query) -> None:
    global connection
    cursor = connection.cursor()
    cursor.execute("INSERT INTO searches (query, user_id, timestamp) VALUES (%s, %s, NOW())", (query, session_id))
    connection.commit()

def get_all_searches(session_id) -> list:
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT query FROM searches WHERE user_id = %s ORDER BY timestamp DESC", (session_id,))
    searches = cursor.fetchall()
    return [search[0] for search in searches]



@app.route("/logout")
def logout():
    try:
        session["is_authenticated"] = False
        flash("You have been logged out successfully.", "success")
        return redirect(url_for("index"))
    except Exception as e:
        print(f"Error during logout: {e}")
        flash("An error occurred during logout.", "error")
        return render_template(redirect(url_for("index")))


@app.route("/", methods=["GET", "POST"])
def index():
    user = session.get("id", None) 
    session.get("username", "Guest")
    session.get("is_authenticated", False)
    session.get("isProUser", "Free")
    if 'session_history' not in session:
        session['session_history'] = []
    if "is_authenticated" not in session:
            session["is_authenticated"] = False
    if "id" not in session:
        
        session["id"] = 0
        session["is_authenticated"] = False
    """if user is not None:
            c_user.is_authenticated = True
            c_user.username = c_user.FindOutUsername()  
            c_user.img_link = c_user.FindOutProfileIMG()
            c_user.isProUser = c_user.FindOutSubscriptionType()"""

    if request.method == "POST":
        if request.form.get("email"):
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirmPassword")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if password != confirm_password:
                flash("Passwords do not match", "error")
                return render_template("index.html", current_user=session)

            try:
                cursor = connection.cursor()
                query = (
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
                )
                cursor.execute(query, (username, email, hashed_password))
                connection.commit()
                flash("Registration successful! You can now log in.", "success")
                return redirect(url_for("index"))
            except Exception as e:
                flash("Registration failed: " + str(e), "error")
                return render_template("index.html", current_user=session)
        else: # if goes to this else, this means its a login duh
            username = request.form.get("username")
            password = request.form.get("password")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (username, hashed_password))

                fetched_user = cursor.fetchone()

                if fetched_user:
                    session["id"] = fetched_user["id"]
                    session["username"] = fetched_user["username"]
                    session["is_authenticated"] = True
                    session["isProUser"] = fetched_user["subscription"]

                    flash("Login successful!", "success")
                    return redirect(url_for("index"))
                else:
                    flash("Invalid username or password", "error")
                    return render_template("index.html", current_user=session)
            except Exception as e:
                print("Error: " + str(e))

    return render_template(
        "index.html", current_user=session )


@app.route("/history", methods=["GET"])
def history():


    
    if id_valid(session_id=session.get("id", 0)):
        server_saved_searches = get_all_searches(session_id=session["id"])

    return render_template("history.html", 
                           current_user=session, 
                           server_saved_searches=server_saved_searches, 
                           session_history=session['session_history'])


@app.route("/about", methods=["GET"])
def about():
    """ser = session.get("id")
    if user is not None:
        c_user.is_authenticated = True
        c_user.username = c_user.FindOutUsername()
        c_user.img_link = c_user.FindOutProfileIMG()
        c_user.isProUser = c_user.FindOutSubscriptionType()"""
    return render_template("index.html", user=user)


@app.route("/contact", methods=["GET"])
def contact():
    return render_template("index.html", user=user)


@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html", 
                           current_user=session, 
                           wuf=FindOutTimeAfterCreation(session["id"]))


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")

    search_results = SAE.Search(query=query)

    if id_valid(session["id"]):
        add_to_searches(session["id"], query=query)

    session['session_history'].append(query)

    return render_template(
        "search.html",
        results=search_results,
        current_user=session,
        search_query=query
    )



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

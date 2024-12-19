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


class UserProfile:
    def __init__(
        self,
        is_authenticated=False,
        isProUser=False,
        isGuest=False,
        img_link=default_pfp,
        username="Guest",
        id: int = 0,
    ):
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
        if subscription == "free":
            return "Free"
        elif subscription == "premium" or subscription == None:
            return "Premium"

    def FindOutUsername(self) -> str:
        global connection
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users WHERE id = %s", (self.id,))
        name = cursor.fetchone()
        return name if name else None

    def FindOutProfileIMG(self) -> str:
        global connection
        cursor = connection.cursor()
        cursor.execute("SELECT img FROM users WHERE id = %s", (self.id,))
        pfp = cursor.fetchone()
        return pfp if pfp else default_pfp
    def FindOutTimeAfterCreation(self):
        """
        Find out how long the user has been created for
        """
        global connection
        cursor = connection.cursor()
        cursor.execute("SELECT creation_date FROM users WHERE id = %s", (self.id,))
        created_at = cursor.fetchone()
        if created_at:
            created_at = created_at[0]
            time_diff = datetime.now() - created_at
            days = (time_diff.days % 365) % 30
            return days
        else:
            return "Unknown"


c_user = UserProfile()

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
    cursor.execute("INSERT INTO searches (query, user_id, creation_date) VALUES (%s, %s, NOW())", (query, session_id))
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

        user_id = session.get('id', 0)
        print(f"Attempting to log out user with id: {user_id}")

        
        session.clear()

        # Reset the global user object
        global c_user
        c_user = UserProfile()  # Reset to default guest state
        c_user.is_authenticated = False

   
        flash("You have been logged out successfully.", "success")
        

        return redirect(url_for("index"))
    
    except Exception as e:

        print(f"Error during logout: {e}")
        flash("An error occurred during logout.", "error")
        return render_template(
        "index.html", current_user=c_user, isProUser=c_user.isProUser
    ) # redirect(url_for("index"))


@app.route("/", methods=["GET", "POST"])
def index():
    user = session.get("id", 0)
    if user is not None:
            c_user.is_authenticated = True
            c_user.username = c_user.FindOutUsername()  
            c_user.img_link = c_user.FindOutProfileIMG()
            c_user.isProUser = c_user.FindOutSubscriptionType()

    if request.method == "POST":
        if request.form.get("email"):
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirmPassword")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if password != confirm_password:
                flash("Passwords do not match", "error")
                return render_template("index.html", current_user=c_user)

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
                return render_template("index.html", current_user=c_user)
        else: # if goes to this else, this means its a login duh
            username = request.form.get("username")
            password = request.form.get("password")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (username, hashed_password))

                user = cursor.fetchone()

                if user:

                    session["id"] = user["id"]
                    session["username"] = user["username"]

                    c_user.is_authenticated = True
                    c_user.id = user["id"]
                    c_user.username = user["username"]
                    c_user.img_link = user.get("img", default_pfp)
                    c_user.isProUser = user["subscription"] == "premium"

                    flash("Login successful!", "success")
                    return redirect(url_for("index"))
                else:
                    flash("Invalid username or password", "error")
                    return render_template("index.html", current_user=c_user)
            except Exception as e:
                print("Error: " + str(e))

    return render_template(
        "index.html", current_user=c_user, isProUser=c_user.isProUser
    )


@app.route("/history", methods=["GET"])
def history():
    server_saved_searches = []
    if 'session_history' not in session:
        session['session_history'] = []
    if id_valid(session_id=session.get("id", 0)):
        server_saved_searches = get_all_searches(session_id=session["id"])

    return render_template("history.html", 
                           current_user=c_user, 
                           server_saved_searches=server_saved_searches, 
                           session_history=session['session_history'])


@app.route("/about", methods=["GET"])
def about():
    user = session.get("id")
    if user is not None:
        c_user.is_authenticated = True
        c_user.username = c_user.FindOutUsername()
        c_user.img_link = c_user.FindOutProfileIMG()
        c_user.isProUser = c_user.FindOutSubscriptionType()
    return render_template("index.html", user=user)


@app.route("/contact", methods=["GET"])
def contact():
    user = session.get("id")
    if user is not None:
        c_user.is_authenticated = True
        c_user.username = c_user.FindOutUsername()
        c_user.img_link = c_user.FindOutProfileIMG()
        c_user.isProUser = c_user.FindOutSubscriptionType()
    return render_template("index.html", user=user)


@app.route("/profile", methods=["GET"])
def profile():
    user = session.get("id", 0)
    if user is not None:
        c_user.is_authenticated = True
        c_user.username = c_user.FindOutUsername()
        c_user.img_link = c_user.FindOutProfileIMG()
        c_user.isProUser = c_user.FindOutSubscriptionType()
    return render_template("profile.html", 
                           current_user=c_user, 
                           wuf=c_user.FindOutTimeAfterCreation())


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    user = session.get("id", 0)
    if user is not None and id_valid(user):
        c_user.is_authenticated = True
        c_user.username = c_user.FindOutUsername()
        c_user.img_link = c_user.FindOutProfileIMG()
        c_user.isProUser = c_user.FindOutSubscriptionType()

    search_results = SAE.Search(query=query)

    if 'session_history' not in session:
        session['session_history'] = []
    if id_valid(user):
        add_to_searches(session["id"], query=query)
    session['session_history'].append(query)

    return render_template(
        "search.html",
        results=search_results,
        current_user=c_user,
        search_query=query,
        isProUser=c_user.isProUser,
    )


@app.route("/searches")
def searches():
    user = session.get("id")
    if user is not None:
        c_user.is_authenticated = True
        c_user.username = c_user.FindOutUsername()
        c_user.img_link = c_user.FindOutProfileIMG()
        c_user.isProUser = c_user.FindOutSubscriptionType()
    if 'session_history' not in session:
        session['session_history'] = []
    return render_template("search_stats.html", self_searches=session['session_history'])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

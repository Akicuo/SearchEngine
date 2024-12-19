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

@app.route("/", methods=["GET", "POST"])
def index():

    session.get("username", "Guest")
    session.get("is_authenticated", False)
    session.get("isProUser", "Free")
    session.get("session_history", [])
    if "is_authenticated" not in session:
            session["is_authenticated"] = False
    if "id" not in session:
        
        session["id"] = 0
        session["is_authenticated"] = False
    print(f"Session history: {session['session_history']}")
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
                cursor = sql_model.connection.cursor()
                query = (
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
                )
                cursor.execute(query, (username, email, hashed_password))
                sql_model.connection.commit()
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
                cursor = sql_model.connection.cursor(dictionary=True)
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
    

@app.route("/history", methods=["GET"])
def history():


    
    if sql_model.id_valid(session_id=session.get("id", 0)):
        server_saved_searches = sql_model.get_all_searches(session_id=session["id"])

    return render_template("history.html", 
                           current_user=session, 
                           server_saved_searches=server_saved_searches, 
                           session_history=session['session_history'])


@app.route("/about", methods=["GET"])
def about():
    return redirect(url_for("index"))


@app.route("/contact", methods=["GET"])
def contact():
    return redirect(url_for("index"))


@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html", 
                           current_user=session, 
                           wuf=sql_model.FindOutTimeOfCreation(session["id"]),
                           email=sql_model.FindEmail(session["id"]))


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")

    search_results = SAE.Search(query=query)

    if sql_model.id_valid(session["id"]):
        sql_model.add_to_searches(session["id"], query=query)

    session['session_history'].append(query)

    return render_template(
        "search.html",
        results=search_results,
        current_user=session,
        search_query=query
    )

# API SECTION HERE
@app.route("/api/change-user", methods=["POST"])
def change_user():

    data = request.get_json()

    user_id = data.get('id')
    username = data.get('username')

    if data:
        attempt = sql_model.update_user(user_id, username)
        if attempt:
            session["username"] = username
            return jsonify({"success": True, "message": "Username updated successfully."})
        else:
            return jsonify({"success": False, "message": "Failed to update username."}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

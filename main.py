from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, Response, stream_with_context
import json, time
from datetime import datetime
from models.serper import Serper
import os
from models.mysql import DB as db_model
import hashlib
import json
import uuid
import requests



def read_content(file_path):
    try:
        with open(file_path, "r") as file:
            content = file.read()
            return content
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(0)

bit_to_bool = lambda bit: True if bit == 1 else False

config: dict = {}
with open("config.json", "r") as f:
    config = json.load(f)
    print("Config loaded from file")
    print(config)

SERPER_DEV_API_KEY = config["SERPER_DEV_API_KEY"]

db_model = db_model(host=config["DB_HOST_URL"], user=config["DB_USER"], password=config["DB_PASSWORD"], database="d041e_seai")

try:
    SYSTEM_PROMPT= read_content("prompts/system.txt")
    USER_PROMPT = read_content("prompts/user.txt")
except Exception as e:
    print(f"Error reading prompts: {e}")

serper = Serper(SERPER_DEV_API_KEY)
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = app.secret_key = os.urandom(16)



@app.route("/logout_fg", methods=["GET", "POST"])
def forgot_password():
    global default_pfp
    session["liu"] = None
    return render_template("index.html", session=session)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":

        if request.form.get("email"):
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirm_password = request.form.get("confirmPassword")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if password != confirm_password:
                session["message"] = "Passwords do not match"
                return render_template("register.html", current_user=session)
            if db_model.check_user_exists(username, email):
                session["message"] = "User already exists"
                return render_template("register.html", current_user=session)

            try:
                cursor = db_model.connection.cursor()
                query = (
                    "INSERT INTO users (username, email, password, uuid) VALUES (%s, %s, %s, %s)"
                )
                cursor.execute(query, (username, email, hashed_password, get_random_uuid()))
                db_model.connection.commit()
                session["message"] = "Registration successful! You can now log in.", "success"
                session["user"] = True
                return redirect(url_for("index"))
            except Exception as e:
                print("Registration failed: " + str(e), "error")
                return render_template("index.html", current_user=session)
        else:
            username = request.form.get("username")
            password = request.form.get("password")
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            try:
                cursor = db_model.connection.cursor(dictionary=True)
                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (username, hashed_password))

                fetched_user = cursor.fetchone()

                if fetched_user:
                    session["user"] = True

                    session["message"] = "Login successful!"
                    return redirect(url_for("index"))
                else:
                    session["message"] = "Invalid username or password"
                    return render_template("index.html", current_user=session)
            except Exception as e:
                print("Error: " + str(e))
            

    if "skipTo" in request.args:
        if request.args.get("skipTo").lower() == "register":
            return render_template("register.html", current_user=session)
        elif request.args.get("skipTo").lower() == "login":
            return render_template("login.html", current_user=session)
        else:
            return jsonify({"error": "Invalid skipTo parameter"}), 400
    else:
        return render_template("Login.html", current_user=session)


@app.route("/logout")
def logout():
    try:
        session.clear()
        flash("You have been logged out successfully.", "success")
        return redirect(url_for("index"))
    except Exception as e:
        print(f"Error during logout: {e}")
        flash("An error occurred during logout.", "error")
        return render_template(redirect(url_for("index")))

@app.route("/history", methods=["GET"])
def history():
    server_saved_searches = []
    
    if db_model.id_valid(session_id=session["id"]):
        server_saved_searches = db_model.get_all_searches(session_id=session["id"])
    return render_template("history.html", 
                           current_user=session, 
                           server_saved_searches=server_saved_searches,
                           current_page="history", title="History")


@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html", 
                           current_user=session, 
                           wuf=db_model.FindOutTimeOfCreation(session["id"]),
                           email=db_model.FindEmail(session["id"]),
                           current_page="profile", title="Profile")

@app.route("/search", methods=["GET"])
def search():
    global key, SYSTEM_PROMPT, USER_PROMPT
    query = request.args.get("q")
    cat = request.args.get("cat")
    
    return render_template(
        "search.html", 
        query=query
    )

@app.route("/api/serper", methods=["POST", "GET"])
def api_serper_search():
    cat = request.args.get("cat").lower()
    query = request.args.get("q")
    if  cat in ["bilder", "images"]:
        return jsonify(serper.search_images(query=query))
    elif cat in ["news", "nachrichten"]:
        return jsonify(serper.search_news(query=query))
    elif  cat in ["discover", "all", "alles"]:
        # return jsonify(requests.get(f"https://unsung.cc/api/v1/se-search?q={query}").json())
        return serper.search_discover(query=query)
    elif cat in ["videos"]:
        return jsonify(serper.search_videos(query=query))
    else:
        return jsonify({"error": "Invalid category"}), 400
    

@app.route("/remove-session-message", methods=["POST"])
def remove_session_message():
    if "message" in session:
        session.pop("message")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash,
    Response,
    stream_with_context
)
import json, time
from datetime import datetime
from models.serper import Serper
from models.om import SearchAgentEngine
from models.SearchAI import stream
import os
import models.sql_model as sql_model
import hashlib
import requests
import json
from dotenv import (load_dotenv, dotenv_values)
import regex as re
import uuid
from models.file import read_content



config: dict = {}
with open("config.json", "r") as f:
    config = json.load(f)
    print("Config loaded from file")
    print(config)

NOVITA_API_KEY = config["NOVITA_API_KEY"]
SERPER_DEV_API_KEY = config["SERPER_DEV_API_KEY"]
SUPABASE_API_KEY = config["SUPABASE_API_KEY"]
SUPABASE_URL = config["SUPABASE_URL"]



try:
    SYSTEM_PROMPT= read_content("prompts/system.txt")
    USER_PROMPT = read_content("prompts/user.txt")
except Exception as e:
    print(f"Error reading prompts: {e}")

serper = Serper(SERPER_DEV_API_KEY)
app = Flask(__name__)
app.secret_key = app.secret_key = os.urandom(16)



def get_random_uuid() -> str:
    return str(uuid.uuid4())


@app.route("/", methods=["GET", "POST"])
def index():
    global default_pfp
    session.setdefault("username", None)
    session.setdefault("is_authenticated", False)
    session.setdefault("isProUser", False)
    session.setdefault("id", 0)
    # , current_user=session, current_page="home", title="Home
    return render_template("homesearch.html")


@app.route("/login", methods=["GET", "POST"])
def login():
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
                    "INSERT INTO users (username, email, password, uuid) VALUES (%s, %s, %s, %s)"
                )
                cursor.execute(query, (username, email, hashed_password, get_random_uuid()))
                sql_model.connection.commit()
                flash("Registration successful! You can now log in.", "success")
                return redirect(url_for("index"))
            except Exception as e:
                flash("Registration failed: " + str(e), "error")
                return render_template("index.html", current_user=session)
        else:
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
                    session["uuid"] = fetched_user["uuid"]

                    flash("Login successful!", "success")
                    return redirect(url_for("index"))
                else:
                    flash("Invalid username or password", "error")
                    return render_template("index.html", current_user=session)
            except Exception as e:
                print("Error: " + str(e))


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
    
    if sql_model.id_valid(session_id=session["id"]):
        server_saved_searches = sql_model.get_all_searches(session_id=session["id"])
    return render_template("history.html", 
                           current_user=session, 
                           server_saved_searches=server_saved_searches,
                           current_page="history", title="History")


# threads list var example: [{"title": "unicorn", "created_at": "18:47:00 22-12-2024"}]
@app.route("/threads", methods=["GET"])
def threads():
    return render_template("threads.html", 
                           current_user=session, 
                           threads=sql_model.get_all_threads(session["id"]),
                           current_page="threads", title="Threads")

@app.route("/thread", methods=["GET"])
def thread():
    thread_id = request.args.get("id")
    pass


@app.route("/profile", methods=["GET"])
def profile():
    return render_template("profile.html", 
                           current_user=session, 
                           wuf=sql_model.FindOutTimeOfCreation(session["id"]),
                           email=sql_model.FindEmail(session["id"]),
                           current_page="profile", title="Profile")

@app.route("/search", methods=["GET"])
def search():
    global key, SYSTEM_PROMPT, USER_PROMPT
    query = request.args.get("q")

    return render_template(
        "search.html",
        query=query
    )


# Backend API starts here

@app.route("/api/serper", methods=["POST", "GET"])
def api_serper_search():
    cat = request.args.get("cat", "discover").lower()
    query = request.args.get("q")
    if "images" == cat:
        return jsonify(serper.search_images(query=query))
    elif "news" == cat:
        return jsonify(serper.search_news(query=query))
    elif "discover" == cat:
        return jsonify(serper.search_discover(query=query))
    else:
        return jsonify({"error": "Invalid category"}), 400
        
    


@app.route("/api/threads/create", methods=["POST"])
def api_create_threads():
    user_uuid = request.args.get("arg_uuid")
    originated_search = request.args.get("originated_search")
    assistant_message = request.args.get("assistant_message")
    thread_title = request.args.get("thread_title")
    
    pass

@app.route("/api/threads/remove", methods=["POST"])
def api_remove_threads():
    user_uuid = request.args.get("arg_uuid")
    thread_id = request.args.get("thread_id")
    pass

@app.route("/api/response", methods=["GET"])
def api_response():
    username = request.args.get("username")
    arg_uuid = request.args.get("arg_uuid")
    query = request.args.get("query")

    if username is None or arg_uuid is None or query is None:
        return jsonify({"error": "Missing Parameters"}), 400

    # Validate user credentials
    cursor = sql_model.connection.cursor(dictionary=True)
    query_check = "SELECT * FROM users WHERE username = %s AND uuid = %s"
    cursor.execute(query_check, (username, arg_uuid))
    fetched_user = cursor.fetchone()

    if not fetched_user:
        return jsonify({"error": "Invalid username or arg_uuid"}), 401
    if sql_model.FindOutSubscriptionType(session["id"]) != "Premium":
        return jsonify({"error": "User  is not premium"}), 403

    @stream_with_context
    def generate_response():
        search_results = SAE.Search(query=query)
        
        process_wr = ""
        for result in search_results.get("organic", []):
            if "snippet" in result:
                process_wr += f"Title: {result['title']}\nUrl: {result['link']}\nSnippet: {result['snippet']}\n\n"
        
        New_user_Prompt = USER_PROMPT.replace("[P1]", query).replace("[P2]", process_wr)
        print(New_user_Prompt)

        answer = stream(key, query=New_user_Prompt, system_prompt=SYSTEM_PROMPT)

        return answer

    return Response(generate_response(), mimetype='text/plain')

@app.route("/api/thread-message", methods=["POST"])
def api_threadMessage():
    role = request.args.get("role")
    if role not in ["assistant", "user"] or role is None:
        return jsonify({"error": "Invalid role"}), 400
    message = request.args.get("message")
    if message is None:
        return jsonify({"error": "Missing message"}), 400
    user_uuid = request.args.get("arg_uuid")
    if user_uuid is None or user_uuid not in sql_model.get_all_uuids(): # Create this function later in sql_model file
        return jsonify({"error": "Invalid UUID"}), 400
    sql_model.save_message_to_thread(user_uuid, role, message)  # Create this function later in sql_model file
    
        


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

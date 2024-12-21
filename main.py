from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    session,
    flash,
    Response
)
import json, time
from datetime import datetime
from requests import get, post
from outside_model.om import SearchAgentEngine
from outside_model.SearchAI import get_novita_ai_response
import os
import outside_model.sql_model as sql_model
import hashlib
import requests
import json
from dotenv import load_dotenv
import regex as re
import uuid
load_dotenv()

app = Flask(__name__)
app.secret_key = "2024-BLJ-Projekt"

SAE = SearchAgentEngine(API_Key="LAYLAN-01i2mdabdj3929dk2lem2l2cd1f4762e84d")
default_pfp = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/768px-Default_pfp.svg.png"

key = os.getenv("OPENAI_API_KEY")
if key is None:
    print("Please set an OPENAI_API_KEY with a .env file")
    exit(0)

SYSTEM_PROMPT= """
You are an advanced Retrieval-Augmented Generation (RAG) Information Extraction model. Your task is to analyze the user's query along with the web response to generate comprehensive and informative answers. Your responses should be detailed, articulate, and include relevant links formatted in square brackets like this: '[number][link]'. Only give Answers that are stated in the web response and do not hallucinate

For example, if the user asks about a public figure, your response could look like this:
Example Response:`
``` 
Elon Musk [1][www.example.com] is a prominent entrepreneur known for his roles as the CEO of SpaceX and Tesla [2][www.example.com]. He has significantly impacted the technology and automotive industries.
```
"""

USER_PROMPT = """``
Your task is to synthesize the information from the user's query and the web response into a coherent and informative answer. Ensure that your response is clear and provides value to the user Be sure to include those includes like [1][https://www.example.com] after every or 2 sentences.
```
USER
[P1]
```
->
```
WEB RESPONSE
[P2] Your task is to synthesize the information from the user's query and the web response into a coherent and informative answer. Ensure that your response is clear and provides value to the user.
```
"""
def get_random_uuid() -> str:
    return str(uuid.uuid4())


@app.route("/", methods=["GET", "POST"])
def index():
    global default_pfp
    session.setdefault("username", None)
    session.setdefault("is_authenticated", False)
    session.setdefault("isProUser", False)
    session.setdefault("id", 0)
    session.setdefault("id", "")
    session.setdefault("img", default_pfp)

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

    return render_template("index.html", current_user=session, current_page="home", title="Home")




@app.route("/get-response", methods=["GET"])
def get_response():
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

    if session["isProUser"] != "Premium":
        return jsonify({"error": "User  is not premium"}), 403

    # Start streaming response
    def generate_response():
        search_results = SAE.Search(query=query)
        
        
        process_wr:str=""
        for result in search_results.get("organic"):
            process_wr+= f"Title: {result['title']}\nUrl: {result['link']}\nSnippet:{result['snippet']}\n\n"
        New_user_Prompt = USER_PROMPT.replace("[P1]", query).replace("[P2]", process_wr)
        print(New_user_Prompt)

        answer = get_novita_ai_response(key, query=New_user_Prompt, system_prompt=SYSTEM_PROMPT)["choices"][0]["message"]["content"]


        for chunk in answer.splitlines():
            yield f"{chunk}\n"  
            time.sleep(0.1) 

    return Response(generate_response(), mimetype='text/plain')





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

@app.route("/about", methods=["GET"])
def about():
    return redirect(url_for("index"))

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
    search_results = SAE.Search(query=query)

    

    

    if sql_model.id_valid(session["id"]):
        sql_model.add_to_searches(session["id"], query=query)

    return render_template(
        "search.html",
        results=search_results,
        current_user=session,
        search_query=query,
        current_page="search", title="Search"
    )




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)

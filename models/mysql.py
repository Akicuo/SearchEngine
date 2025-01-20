import mysql.connector

try:
    connection = mysql.connector.connect(
        host="mysql2.webland.ch",
        user="d041e_seai",
        password="seaiSEAI$2024",
        db="d041e_seai",
    )
except mysql.connector.Error as err:
    print(f"Something went wrong: {err}")
else:
    connection.connect()

def FindOutSubscriptionType(id):
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT subscription FROM users WHERE id = %s", (id,))
    try:
        subscription = cursor.fetchone()[0]
        if subscription == "Free":
            return "Free"
        elif subscription == "Premium" or subscription == None:
            return "Premium"
    except:
        return "Free"

def FindOutUsername(id) -> str:
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM users WHERE id = %s", (id,))
    name = cursor.fetchone()[0]
    return name if name else None

def FindOutProfileIMG(id) -> str:
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT img FROM users WHERE id = %s", (id,))
    pfp = cursor.fetchone()[0]
    return pfp if pfp else ""
def FindOutTimeOfCreation(id):
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT creation_date FROM users WHERE id = %s", (id,))
    created_at = cursor.fetchone()
    return created_at[0]




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

def FindEmail(id):
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT email FROM users WHERE id = %s", (id,))
    email = cursor.fetchone()
    return email[0]
def Change_Profile_Picture(img_data, user_id):
    global connection
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET img = %s WHERE id = %s", (img_data, user_id))
    connection.commit()

def get_all_threads(session_id) -> list:
    global connection
    cursor = connection.cursor()
    query = "SELECT thread_id, thread_title, thread_date FROM threads WHERE user_id = %s ORDER BY thread_date DESC"
    cursor.execute(query, (session_id,))
    threads_selected = cursor.fetchall()
    threads = [{"title": thread[1], "id": thread[0], "created_at": thread[2]} for thread in threads_selected]
    return threads

def get_thread_content(thread_id:int) -> dict:
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT TOP 1 FROM threads WHERE thread = %s ORDER BY timestamp DESC", (thread_id,))
    threads_selected = cursor.fetchone()[0]
    return threads_selected

def remove_thread(thread_id: int) -> dict:
    global connection
    cursor = connection.cursor()
    cursor.execute("DELETE FROM threads WHERE thread_id = %s", (thread_id,))
    connection.commit()
    return {"message": "Thread removed successfully"}

def check_user_exists(username, email) -> bool:
    global connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = %s OR email = %s", (username, email))
    p = cursor.fetchone()
    if p is not None:
        return True
    else:
        return False
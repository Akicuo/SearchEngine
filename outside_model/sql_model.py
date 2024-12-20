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
    subscription = cursor.fetchone()[0]
    if subscription == "free":
        return "Free"
    elif subscription == "premium" or subscription == None:
        return "Premium"

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
"""def update_user(current_username, username):

    # Friday 07:45:00: Changed from using ID of the user to the Username due to issues.

    global connection
    cursor = connection.cursor()
    try:
        cursor.execute("UPDATE users SET username = %s WHERE username = %s", (username, current_username))
        connection.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Something went wrong: {err}")
        return False"""
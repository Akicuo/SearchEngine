import mysql.connector

class DB:
    def __init__(self, host, database, user, password):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                db=database,
            )
        except mysql.connector.Error as err:
            print(f"Something went wrong: {err}")
            exit(1)
        else:
            self.connection.connect()

    def FindOutSubscriptionType(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT subscription FROM users WHERE id = %s", (id,))
        try:
            subscription = cursor.fetchone()[0]
            if subscription == "Free":
                return "Free"
            elif subscription == "Premium" or subscription == None:
                return "Premium"
        except:
            return "Free"

    def FindOutUsername(self, id) -> str:
        cursor = self.connection.cursor()
        cursor.execute("SELECT username FROM users WHERE id = %s", (id,))
        name = cursor.fetchone()[0]
        return name if name else None

    def FindOutProfileIMG(self, id) -> str:
        cursor = self.connection.cursor()
        cursor.execute("SELECT img FROM users WHERE id = %s", (id,))
        pfp = cursor.fetchone()[0]
        return pfp if pfp else ""

    def FindOutTimeOfCreation(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT creation_date FROM users WHERE id = %s", (id,))
        created_at = cursor.fetchone()
        return created_at[0]

    def id_valid(self, session_id):   
        cursor = self.connection.cursor()
        cursor.execute("SELECT 1 FROM users WHERE id = %s", (session_id,))
        p = cursor.fetchone()
        if p is not None:
            return True
        else:
            return False

    def add_to_searches(self, session_id, query) -> None:
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO searches (query, user_id, timestamp) VALUES (%s, %s, NOW())", (query, session_id))
        self.connection.commit()

    def get_all_searches(self, session_id) -> list:
        cursor = self.connection.cursor()
        cursor.execute("SELECT query FROM searches WHERE user_id = %s ORDER BY timestamp DESC", (session_id,))
        searches = cursor.fetchall()
        return [search[0] for search in searches]

    def FindEmail(self, id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT email FROM users WHERE id = %s", (id,))
        email = cursor.fetchone()
        return email[0]

    def Change_Profile_Picture(self, img_data, user_id):
        cursor = self.connection.cursor()
        cursor.execute("UPDATE users SET img = %s WHERE id = %s", (img_data, user_id))
        self.connection.commit()

    def get_all_threads(self, session_id) -> list:
        cursor = self.connection.cursor()
        query = "SELECT thread_id, thread_title, thread_date FROM threads WHERE user_id = %s ORDER BY thread_date DESC"
        cursor.execute(query, (session_id,))
        threads_selected = cursor.fetchall()
        threads = [{"title": thread[1], "id": thread[0], "created_at": thread[2]} for thread in threads_selected]
        return threads

    def get_thread_content(self, thread_id: int) -> dict:
        cursor = self.connection.cursor()
        cursor.execute("SELECT TOP 1 FROM threads WHERE thread = %s ORDER BY timestamp DESC", (thread_id,))
        threads_selected = cursor.fetchone()[0]
        return threads_selected

    def remove_thread(self, thread_id: int) -> dict:
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM threads WHERE thread_id = %s", (thread_id,))
        self.connection.commit()
        return {"message": "Thread removed successfully"}

    def check_user_exists(self, username, email) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = %s OR email = %s", (username, email))
        p = cursor.fetchone()
        if p is not None:
            return True
        else:
            return False
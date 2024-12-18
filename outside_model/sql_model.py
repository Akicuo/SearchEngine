import mysql.connector

class Connector:
    def __init__(self, host, user, password,db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
    def connect(self):

            connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            database=self.db,
            password=self.password,
            )
            return connection

    
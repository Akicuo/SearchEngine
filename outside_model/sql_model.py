import mysql.connector

class Connector:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

        mydb = mysql.connector.connect(
  host=self.host,
  user=self.user,
  password=self.password
)
        return mydb

    
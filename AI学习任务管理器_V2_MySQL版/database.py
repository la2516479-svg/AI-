import mysql.connector


DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "ai_study_manager",
    "use_pure": True
}


class Database:

    def __init__(self):
        self.conn = mysql.connector.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(dictionary=True)

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params)
        self.conn.commit()

    def fetch_all(self, sql, params=None):
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()
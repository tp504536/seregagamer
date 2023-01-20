
import sqlite3
class Database:
    def __init__(self, base):
        self.connection = sqlite3.connect(base)
        self.cursor = self.connection.cursor()

    def users(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            result = self.cursor.execute('INSERT INTO users (id) VALUES (?)', (user_id,))
            return result


    def balance(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE id = ? ", (user_id)).fetchall()
            return result
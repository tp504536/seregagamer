
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
            result = self.cursor.execute('INSERT INTO users (id, balance) VALUES (?,0)', (user_id,))
            return result


    def balance(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT balance FROM users WHERE id = ? ", (user_id,)).fetchall()
            return result

    def balance_update(self,user_id):
        with self.connection:
            result = self.cursor.execute("SELECT balance FROM users WHERE id = ? ", (user_id,)).fetchall()
            a = 150 + int(result[0][0])
            self.cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (a, user_id,))

    def lenuser(self):
        """Считам сколько людей заходило в бота"""
        with self.connection:
            result = self.cursor.execute("SELECT id FROM users;").fetchall()
            return len(result)

    def all_user(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM users').fetchall()
            return result
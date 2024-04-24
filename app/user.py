# app/models/user.py
from flask_login import UserMixin
from app import mysql

class User(UserMixin):
    def __init__(self, id, name, email, role):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

def get_user(user_id):
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute('SELECT * FROM accounts WHERE id = %s', (user_id,))
    user_data = cursor.fetchone()
    cursor.close()

    if not user_data:
        return None

    return User(user_data['id'], user_data['name'], user_data['email'], user_data['role'])

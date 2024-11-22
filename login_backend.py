import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from typing import List, Dict

# Định nghĩa lớp User để đại diện cho người dùng trong hệ thống
class User:
    def __init__(self, user_id = None,  username = None, fullname = None, email = None, birthdate = None, password=None, password_hash=None):
        self.user_id = user_id
        self.username = username  # Tên đăng nhập
        self.fullname = fullname  # Họ tên đầy đủ
        self.email = email        # Email người dùng
        self.birthdate = birthdate  # Ngày sinh
        if password:
            self.password_hash = generate_password_hash(password)  # Mã hóa mật khẩu mới
        else:
            self.password_hash = password_hash  # Sử dụng mật khẩu đã mã hóa

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)  # Kiểm tra mật khẩu có khớp không

# Định nghĩa lớp UserDatabase để quản lý dữ liệu người dùng
class UserDatabase:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), "learning.db")
        self.database_file = db_path

    def add_user(self, user):
        with sqlite3.connect(self.database_file) as conn:
            try:
                # Check if the username or email already exists
                cursor = conn.execute("SELECT COUNT(*) FROM user WHERE username = ? OR email = ?", (user.username, user.email))
                count = cursor.fetchone()[0]
                if count > 0:
                    return False, "Username or email already exists!"

                # Insert the new user
                cursor = conn.execute("""
                    INSERT INTO user (username, fullname, email, birthdate, password_hash)
                    VALUES (?, ?, ?, ?, ?)
                """, (user.username, user.fullname, user.email, user.birthdate, user.password_hash))
                user.user_id = cursor.lastrowid
                return True, "Sign up successfully!"
            except sqlite3.IntegrityError:
                return False, "Username or email already exists!"

    def get_user_by_id(self, user_id):
        with sqlite3.connect(self.database_file) as conn:
            cursor = conn.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(
                    user_id=user_data[0],
                    username=user_data[1],
                    fullname=user_data[2],
                    email=user_data[3],
                    birthdate=user_data[4],
                    password_hash=user_data[5]
                )
            else:
                return None


    def find_user_by_username(self, username):
        with sqlite3.connect(self.database_file) as conn:
            cursor = conn.execute("SELECT * FROM user WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            if user_data:
                return User(
                    user_id=user_data[0],
                    username=user_data[1],
                    fullname=user_data[2],
                    email=user_data[3],
                    birthdate=user_data[4],
                    password_hash=user_data[5]
                )
            else:
                return None

    def find_user_by_email(self, email):
        with sqlite3.connect(self.database_file) as conn:
            cursor = conn.execute("SELECT * FROM user WHERE email = ?", (email,))
            user_data = cursor.fetchone()
            if user_data:
                return User(
                    user_id=user_data[0],
                    username=user_data[1],
                    fullname=user_data[2],
                    email=user_data[3],
                    birthdate=user_data[4],
                    password_hash=user_data[5]
                )
            else:
                return None

    def authenticate_user(self, username, password):
        user = self.find_user_by_username(username)
        if user and user.check_password(password):
            return True, "Log in successfully!"
        return False, "Invalid login information!"
    
    def update_user_password(self, username, new_password):
        with sqlite3.connect(self.database_file) as conn:
            cursor = conn.execute("SELECT * FROM user WHERE username = ?", (username,))
            user = cursor.fetchone()
            cursor.execute("UPDATE user SET password_hash = ? WHERE username = ?", (new_password, username))
            conn.commit()
            return True, 'Change password successfully!'
    def set_user_status_on_by_username(self, username):
        with sqlite3.connect(self.database_file) as conn:
            cursor = conn.execute("SELECT * FROM user WHERE username = ?", (username,))
            user = cursor.fetchone()
            cursor.execute("UPDATE user SET status = 'on' WHERE username = ?", ( username,))
            conn.commit()
            return True, 'Change status successfully!'
    def set_user_status_off_by_username(self, username):
        with sqlite3.connect(self.database_file) as conn:
            cursor = conn.execute("SELECT * FROM user WHERE username = ?", (username,))
            user = cursor.fetchone()
            cursor.execute("UPDATE user SET status = 'off' WHERE username = ?", (username,))
            conn.commit()
            return True, 'Change status successfully!'
user_db = UserDatabase()
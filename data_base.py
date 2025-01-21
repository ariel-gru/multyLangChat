import sqlite3
import os
import hashlib
from passwords_encryption import HashPasswords


class ChatAppDB:
    def __init__(self, db_name="chat_app.db"):
        """
        פעולה בונה: יוצרת חיבור לבסיס הנתונים ומגדירה את הטבלאות הדרושות.
        """
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """
        פעולה פרטית: יוצרת את הטבלאות אם הן אינן קיימות.
        """
        # יצירת טבלת משתמשים
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            preferred_language TEXT DEFAULT 'en'
        )
        """)

        # יצירת טבלת הודעות, שיחה אחת בלבד
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            message_content TEXT NOT NULL,
            eax_tag TEXT NOT NULL,
            language TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users (id)
        )
        """)

        self.conn.commit()

    def save_user(self, username, password):
        """
        שומר יוזר חדש עם סיסמה מוצפנת.
        """
        salt, encrypted_password = HashPasswords.encrypt_password(password)
        try:
            self.cursor.execute("""
            INSERT INTO users (username, password_hash, salt)
            VALUES (?, ?, ?)
            """, (username, encrypted_password, salt))
            self.conn.commit()
            print(f"User '{username}' saved successfully!")
            return f"User '{username}' saved successfully!"
        except sqlite3.IntegrityError:
            print(f"Error: Username '{username}' already exists.")
            return f"Error: Username '{username}' already exists."

    def check_user(self, username, password):
        """
        בודק אם היוזר קיים ואם הסיסמה נכונה.
        """
        self.cursor.execute("""
        SELECT password_hash, salt FROM users WHERE username = ?
        """, (username,))
        result = self.cursor.fetchone()
        if result:
            stored_hash, salt = result
            if HashPasswords.check_password(salt, stored_hash, password):
                return True
        return False

    def send_message(self, sender_id, content, language="en"):
        """
        שולח הודעה לשיחה אחת.
        """
        self.cursor.execute("""
        INSERT INTO messages (sender_id, content, language)
        VALUES (?, ?, ?)
        """, (sender_id, content, language))
        self.conn.commit()

    def get_messages(self):
        """
        מחזיר את כל ההודעות בשיחה אחת.
        """
        self.cursor.execute("""
        SELECT u.username, m.content, m.language, m.timestamp
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        ORDER BY m.timestamp
        """)
        return self.cursor.fetchall()

    def change_language(self, user_id, new_language):
        """
        מעדכן את השפה המועדפת של המשתמש לפי ה-ID.
        """
        self.cursor.execute("""
        UPDATE users SET preferred_language = ? WHERE id = ?
        """, (new_language, user_id))
        self.conn.commit()
        print(f"Preferred language for user with ID '{user_id}' updated to '{new_language}'.")
    
    def get_user_id(self, username):
        """
        מחזירה את ה-ID של המשתמש לפי שם המשתמש.
        """
        self.cursor.execute("""
        SELECT id FROM users WHERE username = ?
        """, (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  #בוחר את הראשון כי tuple
        return None  
    
    def close(self):
        """
        סוגרת את חיבור בסיס הנתונים.
        """
        self.conn.close()


# דוגמה לשימוש בקוד:
db = ChatAppDB()

# שמירת משתמשים חדשים
db.save_user("user1222", "secure_password")
db.save_user("user1223", "another_password")

# בדיקת משתמש
print(db.check_user("user1222", "secure_password"))
print(db.get_user_id("user1222"))
print(db.check_user("user1223", "wrong_password"))

# שליחת הודעות
db.send_message(1, "Hello, this is the first message!", "en")
db.send_message(2, "Hi, I'm responding to your message.", "en")

# קבלת כל ההודעות בשיחה
messages = db.get_messages()
for message in messages:
    print(message[1])

db.close()

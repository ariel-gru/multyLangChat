import sqlite3
import os
import hashlib
from app.passwords_encryption import HashPasswords


class ChatAppDB:
    def __init__(self, db_name="chat_app.db"):
        """
        Creates a connection to the database and defines the tables.
        """
        self.db_dir = 'database'
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
        
        self.db_path = os.path.join(self.db_dir, db_name)
        
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            preferred_language TEXT DEFAULT 'en'
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users (id)
        )
        """)

        self.conn.commit()

    def save_user(self, username, password):
       
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
       
        self.cursor.execute("""
        SELECT password_hash, salt FROM users WHERE username = ?
        """, (username,))
        result = self.cursor.fetchone()
        if result:
            stored_hash, salt = result
            if HashPasswords.check_password(salt, stored_hash, password):
                return True
        return False

    def send_message(self, sender_id, content):
       
        self.cursor.execute("""
        INSERT INTO messages (sender_id, content)
        VALUES (?, ?)
        """, (sender_id, content))
        self.conn.commit()

    def get_messages(self):
      
        self.cursor.execute("""
        SELECT u.username, m.content, m.timestamp
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        ORDER BY m.timestamp
        """)
        return self.cursor.fetchall()

    def change_language(self, user_id, new_language):
        
        self.cursor.execute("""
        UPDATE users SET preferred_language = ? WHERE id = ?
        """, (new_language, user_id))
        self.conn.commit()
        print(f"Preferred language for user with ID '{user_id}' updated to '{new_language}'.")
    
    def get_user_id(self, username):
        
        self.cursor.execute("""
        SELECT id FROM users WHERE username = ?
        """, (username,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  #בוחר את הראשון כי tuple
        return None  
    
    def close(self):
       
        self.conn.close()



if __name__ == "__main__":
    db = ChatAppDB()

    db.save_user("user1222", "secure_password")
    db.save_user("user1223", "another_password")

    print(db.check_user("user1222", "secure_password"))
    print(db.get_user_id("user1222"))
    print(db.check_user("user1223", "wrong_password"))

    db.send_message(1, "Hello, this is the first message!")
    db.send_message(2, "Hi, I'm responding to your message.")

    messages = db.get_messages()
    for message in messages:
        print(message[1])

    db.close()

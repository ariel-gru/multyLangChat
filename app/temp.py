








 # בדיקת שם משתמש וסיסמה (שימו לב שזו לא בדיקה אמיתית, אלא רק לצורך הדגמה)
        if username == "admin" and password == "password":
            self.close()  # סגור את חלון הלוגין
            self.chat_window = ChatApp()  # יצירת אפליקציה חדשה של צ'אט
            self.chat_window.show()  # הצגת חלון הצ'אט
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password", QMessageBox.Ok)
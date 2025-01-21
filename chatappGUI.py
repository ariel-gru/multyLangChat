import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget 

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat App")
        self.resize(400, 600)
        
        # יוצר לייאוט שמכיל את כל הרכיבים של הצ'אט
        self.chat_layout = QVBoxLayout()
        
        # יצירת דף התחברות (בינתיים אינו בשימוש)
        self.login_page = QVBoxLayout()
        
        # תיבת טקסט לתצוגת השיחות
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)  # הופכת את התיבה לקריאה בלבד
        self.chat_layout.addWidget(self.chat_display)
        
        # שדה להזנת הודעה חדשה
        self.input_field = QLineEdit()
        self.chat_layout.addWidget(self.input_field)
        
        # כפתור לשליחת הודעות
        self.send_button = QPushButton("Send")
        self.chat_layout.addWidget(self.send_button)
        
        # חיבור הכפתור לפונקציית השליחה
        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)
        
        # יצירת תצוגת חלון מרכזית
        container = QWidget()
        container.setLayout(self.chat_layout)
        self.setCentralWidget(container)

    def send_message(self):
        message = self.input_field.text()
        if message:
            # הוספת ההודעה לתצוגה
            self.chat_display.append(f"You: {message}")
            self.input_field.clear()  # ניקוי שדה הקלט

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget 

class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat App")
        self.resize(400, 600)
        
        self.chat_layout = QVBoxLayout()
        
        self.login_page = QVBoxLayout()
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)  # הופכת את התיבה לקריאה בלבד
        self.chat_layout.addWidget(self.chat_display)
        
        self.input_field = QLineEdit()
        self.chat_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Send")
        self.chat_layout.addWidget(self.send_button)
        
        self.send_button.clicked.connect(self.send_message)
        self.input_field.returnPressed.connect(self.send_message)
        
        container = QWidget()
        container.setLayout(self.chat_layout)
        self.setCentralWidget(container)

    def send_message(self):
        message = self.input_field.text()
        if message:
            self.chat_display.append(f"You: {message}")
            self.input_field.clear()  

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())

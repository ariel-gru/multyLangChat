from translator import Translator
import sys
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget, QLabel, QScrollArea, QHBoxLayout, QMenu, QAction , QLineEdit,QMessageBox
from datetime import datetime
from languages import languages
import client
import json
import threading
import asyncio

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.resize(300, 200)
        self.center_window()
        self.client=client.client()
        self.language=None
        self.username=""

        # יצירת הלייאוטים
        self.main_layout = QVBoxLayout()
        self.input_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()

        # יצירת אלמנטים של לוגין
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Enter your username")

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")

        # כפתור כניסה
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)

        # כפתור רישום
        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register)

        # הוספת אלמנטים ללייאוטים
        self.input_layout.addWidget(self.username_label)
        self.input_layout.addWidget(self.username_input)
        self.input_layout.addWidget(self.password_label)
        self.input_layout.addWidget(self.password_input)

        self.buttons_layout.addWidget(self.login_button)
        self.buttons_layout.addWidget(self.register_button)

        # הוספת הלייאוטים לחלון הראשי
        self.main_layout.addLayout(self.input_layout)
        self.main_layout.addLayout(self.buttons_layout)

        self.language_button = QPushButton("Choose your language")
        self.language_button.setMenu(self.create_language_menu())

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save)

        self.save_layout =QVBoxLayout()
        self.save_layout.addWidget(self.language_button)
        self.save_layout.addWidget(self.save_button)

        # יצירת ווידג'ט וסט של הלייאוטים
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
    
    def save(self):
        if self.language:
            self.client.change_lang(self.language)
            chat=ChatApp(self.username,self.client,self.language)
            chat.show()
            self.close()
        else:
            self.show_error("You need to choose a language", "Please choose language.")
    
    def create_language_menu(self):
        menu = QMenu(self.language_button)
        for language in languages:
            action = QAction(language, self)
            action.triggered.connect(lambda checked, lang=language: self.select_language(lang))
            menu.addAction(action)
        return menu
    
    def select_language(self, language):
        self.language = language
        self.language_button.setText(language)
    
    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = QApplication.desktop().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def login(self):
        username = self.username_input.text()
        self.username = username
        password = self.password_input.text()
        if not username and not password:
            self.show_error("Both fields are required!", "Please enter your username and password.")
        elif not username:
            self.show_error("Username field is empty!", "Please enter your username.")
        elif not password:
            self.show_error("Password field is empty!", "Please enter your password.")
        else:
            data = {
                    "username":username,
                    "password":password,
                    "operation":"login"
                }
            json_data = json.dumps(data)
            connected , language = self.client.login(json_data)
            if connected:
                self.language = language
                chat=ChatApp(self.username,self.client,self.language)
                chat.show()
                self.close()
               
            else:
                self.show_error("Cant log in","Wrong username or password")
        
    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username and not password:
            self.show_error("Both fields are required!", "Please enter your username and password.")
        elif not username:
            self.show_error("Username field is empty!", "Please enter your username.")
        elif not password:
            self.show_error("Password field is empty!", "Please enter your password.")
        else:
            data = {
                    "username":username,
                    "password":password,
                    "operation":"register"
                }
            json_data = json.dumps(data)
            if self.client.register(json_data):
                container = QWidget()
                container.setLayout(self.save_layout)
                self.setCentralWidget(container)
            else:
                self.show_error("Username already exists","choose another username")
    
    def show_error(self, title, message):
        # הצגת הודעת שגיאה באמצעות QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()


class ChatMessage:
    def __init__(self, content, sender="You"):
        self.content = content
        self.sender = sender
        self.timestamp = self.get_send_time()
    
    def get_sender(self):
        return self.sender
    
    def get_content(self):
        return self.content
    
    def get_send_time(self):
        return datetime.now().strftime("%H:%M")

    def format(self):
        return f"{self.content}" if self.sender == "You" else f"{self.sender}: {self.content}"


class ChatApp(QMainWindow):
    def __init__(self,username,client:client,preferd_language="English"):
        super().__init__()
        self.setWindowTitle("Chat App")
        self.resize(400, 600)
        self.translator = Translator()
        self.messages = []
        self.username=username
        self.preferd_language=preferd_language
        self.client = client


        # chat layout
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignTop)

        # auto scroll
        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(self.chat_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)

        #input-field
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.setFixedHeight(50)

        #send
        self.send_button = QPushButton("Send")
        self.language_button = QPushButton(preferd_language)
        
        #send-func
        self.send_button.clicked.connect(self.send_message)
        self.language_button.setMenu(self.create_language_menu())

        #but layouts
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.send_button)
        buttons_layout.addWidget(self.language_button)

        #buttons and input field
        lower_layout = QHBoxLayout()
        lower_layout.addWidget(self.input_field)
        lower_layout.addLayout(buttons_layout)

        # main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(lower_layout)


        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # enter
        self.input_field.installEventFilter(self)
        self.send_button.installEventFilter(self)

        threading.Thread(target=self.recive_message, daemon=True).start()
    
    
    def recive_message(self):
        def handle_message(message):
            print(message)
            sender = message.split(":")[0]
            message = message.split(":",1)[1]
            print(sender)
            print(message)
            message=self.translator.translate(message,languages[self.preferd_language])
            chat_message = ChatMessage(message, sender)
            # צריך להריץ את הצגת ההודעה בthread הראשי של Qt
            self.display_message_safe(chat_message)
        
        self.client.get_msg(handle_message)

    def create_language_menu(self):
        menu = QMenu(self.language_button)
        for language in languages:
            action = QAction(language, self)
            action.triggered.connect(lambda checked, lang=language: self.select_language(lang))
            menu.addAction(action)
        self.language_button.setText(self.preferd_language)
        return menu

    def select_language(self, language):
        self.language_button.setText(language)
        self.preferd_language = language
        self.translate_all_messages(language)
        
    
    def translate_all_messages(self,language):
        for  message in self.messages:
                if message[1] != language:
                    print(message[0].text())
                    sender = message[0].text().split(":",1)[0] if message[2] == 1 else None
                    translated_text=self.translator.translate(message[0].text().split(":",1)[1],languages[language]) if sender else self.translator.translate(message[0].text(),languages[language]) 
                    if message[2] == 1:
                        message[0].setText(sender+":"+translated_text)
                        self.messages[self.messages.index(message)] = (message[0],language,1)
                    else:
                        message[0].setText(translated_text)
                        self.messages[self.messages.index(message)] = (message[0],language,0)
                    
    
    def send_message(self):
        message_content = self.input_field.toPlainText().strip()
        if message_content:
            message = ChatMessage(content=message_content)
            self.display_message(message,0)
            self.client.snd_msg(message_content, self.username)  # שליחה לשרת
            self.input_field.clear()

    def display_message_safe(self, message):
        # Qt לא מאפשר עדכון UI מthread משני
        # לכן נשתמש ב-invokeMethod כדי לעדכן את ה-UI בthread הראשי
        from PyQt5.QtCore import QMetaObject, Qt, Q_ARG, pyqtSlot
        QMetaObject.invokeMethod(self, "display_message", 
                            Qt.QueuedConnection,
                            Q_ARG(ChatMessage, message),
                            Q_ARG(int,1))
    
    @pyqtSlot(ChatMessage,int)
    def display_message(self, message,sender):
        # message label
        message_label = QLabel(message.format())
        self.messages.append((message_label,None,sender))
        time_label = QLabel(message.get_send_time())
        color ="#4ee565" if message.get_sender() == "You" else "#afafaf"
       
        message_label.setStyleSheet(f"""
            background-color: {color};
            border-radius: 10px;
            padding: 8px;
            margin: 0px;
            font-size: 12px;
        """)
        time_label.setStyleSheet(f"""
            font-size: 10px;
            color: #888888;
            margin-left: 5px;
            vertical-align: top;
        """)
        message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
        # message layout
        message_layout = QHBoxLayout()
        
        if message.get_sender() == "You":
            message_layout.setAlignment(Qt.AlignRight)
        else:
            message_layout.setAlignment(Qt.AlignLeft)
        
        message_layout.addWidget(message_label)
        message_layout.addWidget(time_label)

        # message widget
        message_widget = QWidget()
        message_widget.setLayout(message_layout)
        
        self.chat_layout.addWidget(message_widget)
        
    

    def keyPressEvent(self, event):
        # enter
        if event.key() == Qt.Key_Return:
            self.send_message()

    def eventFilter(self, obj, event):
        if event.type() == event.KeyPress and event.key() == Qt.Key_Return:
            if event.modifiers() == Qt.ShiftModifier:
                return super().eventFilter(obj, event)
            self.send_message()
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
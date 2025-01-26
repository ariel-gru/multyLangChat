from translator import Translator
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget, QLabel, QScrollArea, QHBoxLayout, QMenu, QAction
from datetime import datetime
from languages import languages


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
    def __init__(self,preferd_language="English"):
        super().__init__()
        self.setWindowTitle("Chat App")
        self.resize(400, 600)
        self.translator = Translator()
        self.messages = []


        # יצירת תצוגת הצ'אט
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignTop)

        # גלילה עבור תצוגת הצ'אט
        self.scroll_area = QScrollArea()
        self.scroll_area_widget = QWidget()
        self.scroll_area_widget.setLayout(self.chat_layout)
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area.setWidgetResizable(True)

        # שדה הקלט (שדה טקסט מרובה שורות)
        self.input_field = QTextEdit()
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.setFixedHeight(50)

        # כפתור שליחה
        self.send_button = QPushButton("Send")
        self.language_button = QPushButton(preferd_language)
        
        # יצירת תפריט עבור כפתור L
        self.send_button.clicked.connect(self.send_message)
        self.language_button.setMenu(self.create_language_menu())

        # Layout של הכפתורים
        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.send_button)
        buttons_layout.addWidget(self.language_button)

        lower_layout = QHBoxLayout()
        lower_layout.addWidget(self.input_field)
        lower_layout.addLayout(buttons_layout)

        # פריסה ראשית
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        main_layout.addLayout(lower_layout)

        # הגדרת הפריסה לממשק הראשי
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # הוספת מאזין למקש "Enter" בכל הווידג'טים
        self.input_field.installEventFilter(self)
        self.send_button.installEventFilter(self)

    def create_language_menu(self):
        menu = QMenu(self.language_button)
        for language in languages:
            action = QAction(language, self)
            action.triggered.connect(lambda checked, lang=language: self.select_language(lang))
            menu.addAction(action)
        return menu

    def select_language(self, language):
        self.translate_all_messages(language)
        self.language_button.setText(language)
    
    def translate_all_messages(self,language):
        for  message in self.messages:
                if message[1] != language:
                    print(message[0].text())
                    translated_text=self.translator.translate(message[0].text(),languages[language])
                    message[0].setText(translated_text)
                    self.messages[self.messages.index(message)] = (message[0],language)
                    

    def send_message(self):
        message_content = self.input_field.toPlainText().strip()
        if message_content:
            # יצירת אובייקט הודעה
            message = ChatMessage(content=message_content)

            # הצגת ההודעה בממשק
            self.display_message(message)

            # ניקוי שדה הקלט
            self.input_field.clear()

            # גלילה אוטומטית להודעה האחרונה
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

            # לשים את הסמן בשדה ההקלדה לאחר שליחה
            self.input_field.setFocus()

    def display_message(self, message):
        # יצירת תווית להודעה
        message_label = QLabel(message.format())
        self.messages.append((message_label,None))
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
        
        # Layout לכל הודעה
        message_layout = QHBoxLayout()
        
        if message.get_sender() == "You":
            message_layout.setAlignment(Qt.AlignRight)
        else:
            message_layout.setAlignment(Qt.AlignLeft)
        
        message_layout.addWidget(message_label)
        message_layout.addWidget(time_label)

        # Widget עבור כל הודעה
        message_widget = QWidget()
        message_widget.setLayout(message_layout)
        # הוספת ההודעה לתצוגת הצ'אט
        self.chat_layout.addWidget(message_widget)
        
    

    def keyPressEvent(self, event):
        # אם נלחץ Enter
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
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())

from translator import Translator
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QStackedWidget, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget, QLabel, QScrollArea, QHBoxLayout, QMenu, QAction, QDesktopWidget
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
        self.resize(400, 500)
        self.translator = Translator()
        self.messages = []
        self.max_characters = 200
        self.center_window()
        self.stacked_widget = QStackedWidget()

        self.login_page = QWidget()
        self.chat_page = QWidget()

        self.login_page.setLayout()
        self.chat_page.setLayout(self.chat_layout)


        #login layout
        self.login_layout = QVBoxLayout()
        self.chat_layout.setAlignment(Qt.AlignTop)

        



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
        self.input_field.textChanged.connect(self.check_character_limit)
        

        self.char_count_label = QLabel(f"{self.max_characters} characters remaining")

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
        lower_layout.addWidget(self.char_count_label)

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

    def center_window(self):
        # קבלת מסגרת המסך
        frame_geometry = self.frameGeometry()
        # קבלת המרכז של המסך
        screen_center = QDesktopWidget().availableGeometry().center()
        # מיקום החלון במרכז המסך
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())

    def check_character_limit(self):  # פונקציה חדשה לבדיקה והגבלת מספר התווים
        current_text = self.input_field.toPlainText()
        remaining_characters = self.max_characters - len(current_text)
        
        # עדכון הטקסט בתווית
        self.char_count_label.setText(f"{max(remaining_characters, 0)} characters remaining")  # עדכון מספר תווים שנותרו
        
        # אם חרגנו מהמגבלה, חתוך את הטקסט
        if len(current_text) > self.max_characters:
            self.input_field.setText(current_text[:self.max_characters])
            cursor = self.input_field.textCursor()
            cursor.movePosition(cursor.End)
            self.input_field.setTextCursor(cursor)

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
                    
    def check_character_limit(self):
        current_text = self.input_field.toPlainText()
        remaining_characters = self.max_characters - len(current_text)
        
        # עדכון הטקסט בתווית
        self.char_count_label.setText(f"{max(remaining_characters, 0)} characters remaining")
        
        # אם חרגנו מהמגבלה, חתוך את הטקסט
        if len(current_text) > self.max_characters:
            self.input_field.setText(current_text[:self.max_characters])
            cursor = self.input_field.textCursor()
            cursor.movePosition(cursor.End)
            self.input_field.setTextCursor(cursor)

    def send_message(self):
        message_content = self.input_field.toPlainText().strip()
        if message_content:
            # message obj
            message = ChatMessage(content=message_content)
            self.display_message(message)

            self.input_field.clear()
            
            #auto scroll
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

            # putting the saman in the input field
            self.input_field.setFocus()

    def display_message(self, message):
        # message label
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
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())

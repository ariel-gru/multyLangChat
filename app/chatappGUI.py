import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget, QLabel, QScrollArea


class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat App")
        self.resize(400, 600)

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
        self.input_field.setFixedHeight(50)  # הגדרת גובה התחלה לשדה הקלט

        # כפתור שליחה
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        # פריסה ראשית
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.input_field)
        main_layout.addWidget(self.send_button)

        # הגדרת הפריסה לממשק הראשי
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # הוספת מאזין למקש "Enter" בכל הווידג'טים
        self.input_field.installEventFilter(self)
        self.send_button.installEventFilter(self)

    def send_message(self):
        message = self.input_field.toPlainText().strip()
        if message:
            # יצירת תווית להודעה
            message_label = QLabel(message)
            message_label.setStyleSheet("""
                background-color: #4ee565;
                border-radius: 10px;
                padding: 8px;
                margin: 0px;
                font-size: 12px;
            """)
            message_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
            # יישור לימין תמיד
            message_label.setAlignment(Qt.AlignRight)

            # Layout לכל הודעה
            message_layout = QVBoxLayout()
            message_layout.setAlignment(Qt.AlignRight)
            message_layout.addWidget(message_label)

            # Widget עבור כל הודעה
            message_widget = QWidget()
            message_widget.setLayout(message_layout)

            # הוספת ההודעה לתצוגת הצ'אט
            self.chat_layout.addWidget(message_widget)
            self.input_field.clear()

            # גלילה אוטומטית להודעה האחרונה
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

            # לשים את הסמן בשדה ההקלדה לאחר שליחה
            self.input_field.setFocus()

    def keyPressEvent(self, event):
        # אם נלחץ Enter
        if event.key() == Qt.Key_Return:
            self.send_message()# לזכור שהיה אתגר בלסדר אופציה לשליחה עם אנטר ושזה גרם לכך שלא יהיה אפשר לרדת שורה בשיפט אנטר ושיט
            
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

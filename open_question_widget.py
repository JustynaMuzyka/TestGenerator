from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QTextEdit,
    QWidget,
    QVBoxLayout,
    )

from database import database
from database import Question

class OpenQuestionWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.question = Question(questionType='OPEN')

        self.widgets = {
            'question' : QTextEdit()
            }

        self.widgets['question'].setStyleSheet("font-size: 13px; background: '#ffffff'")
        self.widgets['question'].setPlaceholderText("Enter question")
        self.widgets['question'].textChanged.connect(self.on_add_question)

        layout = QVBoxLayout()
        layout.addWidget(self.widgets['question'])
        self.setLayout(layout)

    def on_add_question(self):
        self.question.questionText = self.widgets['question'].toPlainText()

    def on_next(self, test):
        if self.question.questionText:
            idTest = database.insert_test(test)
            idQuestion = database.insert_question(self.question, idTest)
            
            database.commit()
            return True

        return False

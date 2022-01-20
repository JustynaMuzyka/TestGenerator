from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QIntValidator
from PySide6.QtWidgets import (
    QTextEdit,
    QLineEdit,
    QWidget,
    QVBoxLayout,
    QHBoxLayout
    )

from database import database
from database import Question

class OpenQuestionWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.question = Question(questionType='OPEN')

        self.widgets = {
            'question' : QTextEdit(),
            'time' : QLineEdit()
            }

        self.widgets['question'].setStyleSheet("font-size: 18px; background: '#ffffff'")
        self.widgets['question'].setPlaceholderText("Enter question")
        self.widgets['question'].textChanged.connect(self.on_add_question)

        self.widgets['time'].setStyleSheet("font-size: 14px; background: '#ffffff'")
        self.widgets['time'].setPlaceholderText("Enter time")
        self.widgets['time'].setValidator(QIntValidator(1, 600))
        self.widgets['time'].editingFinished.connect(self.on_add_time)
        self.widgets['time'].setMaximumWidth(70)

        questionWithTimeLayout = QHBoxLayout()
        questionWithTimeLayout.addWidget(self.widgets['question'])
        questionWithTimeLayout.addWidget(self.widgets['time'])
        questionWithTimeLayout.setAlignment(self.widgets['time'], Qt.AlignTop)

        layout = QVBoxLayout()
        layout.addLayout(questionWithTimeLayout)
        self.setLayout(layout)

    def on_add_question(self):
        self.question.questionText = self.widgets['question'].toPlainText()

    def on_add_time(self):
        self.question.questionTime = self.widgets['time'].text()

    def on_next(self, test):
        if self.question.questionText and self.question.questionTime:
            idTest = database.insert_test(test)
            idQuestion = database.insert_question(self.question, idTest)
            
            database.commit()
            return True

        return False

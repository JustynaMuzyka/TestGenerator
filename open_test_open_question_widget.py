from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor, QFont
from PySide6.QtWidgets import (
    QTextEdit,
    QRadioButton,
    QButtonGroup,
    QDialog,
    QLineEdit,
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QPushButton,
    QLabel
    )

from database import database
from database import Answer, Question

class OpenTestOpenQuestionWidget(QWidget):

    def __init__(self, results):

        super().__init__()

        self.widgets = {
            'question' : QLabel(),
            'answer' : QTextEdit(),
            }
        self.answer = ""
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)

        self.widgets['question'].setText(results['question'].questionText)
        self.widgets['question'].setFont(font)

        self.widgets['answer'].setStyleSheet("font-size: 13px; background: '#ffffff'")
        self.widgets['answer'].setPlaceholderText("Enter answer and click confirm")
        self.widgets['answer'].setMaximumHeight(450)
        self.widgets['answer'].textChanged.connect(self.on_add_answer)

        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.widgets['question'])
        self.formLayout.addRow(self.widgets['answer'])

        layout = QVBoxLayout()
        layout.addLayout(self.formLayout)
        self.setLayout(layout)

    def on_add_answer(self):
        self.answer = self.widgets['answer'].toPlainText()

    def on_next(self, file, isTimeout):
        if not isTimeout and self.answer:
            file.write("Question: " + self.widgets['question'].text() + "\n")
            file.write("Answer - " + self.answer + "\n\n")
            return True
        elif isTimeout and not self.answer:
            file.write("Question: " + self.widgets['question'].text() + "\n")
            file.write("Answer - " + "LEFT EMPTY\n\n")
            return True

        return False

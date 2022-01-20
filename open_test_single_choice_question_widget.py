from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor, QFont
from PySide6.QtWidgets import (
    QRadioButton,
    QButtonGroup,
    QDialog,
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QPushButton,
    QLabel
    )

from database import database
from database import Answer, Question

class OpenTestSingleChoiceQuestionWidget(QWidget):

    def __init__(self, results):
        super().__init__()

        self.widgets = {
            'question' : QLabel(),
            'answers' : QButtonGroup(),
            }
        self.idCheckedAnswer = 0 
        self.correctAnswer = ""
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)

        self.widgets['question'].setText(results['question'].questionText)
        self.widgets['question'].setFont(font)

        for answer in results['answers']:
            button = QRadioButton(answer.answerText)
            self.widgets['answers'].addButton(button)
            if answer.isCorrect == True:
                self.correctAnswer = answer.answerText

        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.widgets['question'])
        for button in self.widgets['answers'].buttons():
            button.setStyleSheet("font-size: 16px")
            self.formLayout.addWidget(button)

        layout = QVBoxLayout()
        layout.addLayout(self.formLayout)
        self.setLayout(layout)

    def on_next(self, file, isTimeout):
        self.idCheckedAnswer = self.widgets['answers'].checkedId()

        if not isTimeout and self.idCheckedAnswer < -1:
            file.write("Question: " + self.widgets['question'].text() + "\n")
            button = self.widgets['answers'].button(self.idCheckedAnswer)
            if button.text() == self.correctAnswer:
                file.write("Answer - " + button.text() + "   CORRECT\n\n")
            else:
                file.write("Answer - " + button.text() + "   WRONG\n\n")
            
            return True
        elif isTimeout and self.idCheckedAnswer == -1:
            file.write("Question: " + self.widgets['question'].text() + "\n")
            file.write("Answer - " + "LEFT EMPTY\n\n")
            return True

        return False

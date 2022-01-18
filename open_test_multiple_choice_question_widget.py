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

class OpenTestMultipleChoiceQuestionWidget(QWidget):

    def __init__(self, results):
        super().__init__()
        
        self.widgets = {
            'question' : QLabel(),
            'answers' : QButtonGroup(),
            }
        self.correctAnswer = []
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)

        self.widgets['question'].setText(results['question'].questionText)
        self.widgets['question'].setFont(font)

        buttonId = 0
        self.widgets['answers'].setExclusive(False)
        for answer in results['answers']:
            button = QRadioButton(answer.answerText)
            self.widgets['answers'].addButton(button, buttonId)
            buttonId += 1
            if answer.isCorrect == True:
                self.correctAnswer.append(answer.answerText)
        
        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.widgets['question'])
        for button in self.widgets['answers'].buttons():
            self.formLayout.addWidget(button)

        layout = QVBoxLayout()
        layout.addLayout(self.formLayout)
        self.setLayout(layout)
    
    def on_next(self, file):
        checkedAnswersIds = []
        for i, button in enumerate(self.widgets['answers'].buttons()):
            if button.isChecked():
                checkedAnswersIds.append(i)
        
        if checkedAnswersIds:
            file.write("Question: " + self.widgets['question'].text() + "\n")

            for checkedId in checkedAnswersIds:
                button = self.widgets['answers'].button(checkedId)
                if button.text() in self.correctAnswer:
                    file.write("Answer - " + button.text() + "   CORRECT\n")
                else:
                    file.write("Answer - " + button.text() + "   WRONG\n")
            file.write("\n")
            return True

        return False

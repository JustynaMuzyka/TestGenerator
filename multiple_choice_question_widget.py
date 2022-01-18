from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QRadioButton,
    QButtonGroup,
    QDialog,
    QLineEdit,
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QPushButton
    )

from database import database
from database import Answer, Question

class MultipleChoiceQuestionWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.question = Question(questionType='MULTIPLE')
        self.answers = []

        self.widgets = {
            'question' : QLineEdit(),
            'answers' : QButtonGroup(),
            'addAnswer' : QPushButton("Add answer")
            }

        self.widgets['addAnswer'].setStyleSheet("font-size: 15px; background: '#40C742'")
        self.widgets['addAnswer'].setCursor(QCursor(Qt.PointingHandCursor))
        self.widgets['question'].setStyleSheet("font-size: 13px; background: '#ffffff'")
        self.widgets['question'].setPlaceholderText("Enter question")
        self.widgets['question'].editingFinished.connect(self.on_add_question)

        self.widgets['answers'].setExclusive(False)
        
        self.widgets['addAnswer'].clicked.connect(self.on_add_answer)

        self.formLayout = QFormLayout()
        self.formLayout.addRow(self.widgets['question'])
        self.formLayout.addRow(self.widgets['addAnswer'])

        layout = QVBoxLayout()
        layout.addLayout(self.formLayout)
        self.setLayout(layout)

    def on_add_question(self):
        self.question.questionText = self.widgets['question'].text()

    def on_add_answer(self):
        self.answerLineEdit = QLineEdit()
        self.answerLineEdit.setPlaceholderText("Enter answer")
        self.answerLineEdit.setStyleSheet("background: '#ffffff';")

        confirmAnswerButton = QPushButton("OK")
        confirmAnswerButton.setCursor(QCursor(Qt.PointingHandCursor))
        confirmAnswerButton.setStyleSheet("background: '#40C742'")
        confirmAnswerButton.clicked.connect(self.confirm_answer)
        confirmAnswerButton.setCursor(QCursor(Qt.PointingHandCursor))

        formLayout = QFormLayout()
        formLayout.addRow(self.answerLineEdit)
        formLayout.addRow(confirmAnswerButton)
    
        self.createAnswerDialog = QDialog()
        self.createAnswerDialog.setStyleSheet("background: #82FF84;")
        self.createAnswerDialog.setWindowTitle("Create answer")
        self.createAnswerDialog.setWindowModality(Qt.ApplicationModal)
        self.createAnswerDialog.setLayout(formLayout)
        self.createAnswerDialog.exec()

        if self.createAnswerDialog.result() == QDialog.Accepted:
            buttonToAdd = QRadioButton(self.answerLineEdit.text())
            idButton = len(self.widgets['answers'].buttons())
            
            self.formLayout.insertRow(self.formLayout.count() - 1, buttonToAdd)
            self.widgets['answers'].addButton(buttonToAdd, idButton)
            self.answers.append(Answer(self.answerLineEdit.text()))

    def confirm_answer(self):
        if self.answerLineEdit.text():
            self.createAnswerDialog.accept()

    def on_next(self, test):
        correctAnswersIds = []
        for i, button in enumerate(self.widgets['answers'].buttons()):
            if button.isChecked():
                correctAnswersIds.append(i)
        
        if self.question.questionText and self.answers and correctAnswersIds:
            idTest = database.insert_test(test)
            idQuestion = database.insert_question(self.question, idTest)
            
            for i, answer in enumerate(self.answers):
                if i in correctAnswersIds:
                    answer.isCorrect = True
                database.insert_answer(answer, idQuestion)

            database.commit()
            return True

        return False


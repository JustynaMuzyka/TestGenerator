from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor, QIntValidator, QPixmap, QIcon
from PySide6.QtWidgets import (
    QRadioButton,
    QButtonGroup,
    QDialog,
    QLineEdit,
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
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
            'time' : QLineEdit(),
            'answers' : QButtonGroup(),
            'addAnswer' : QPushButton()
            }
        addAnswerButtonIcon = QIcon()
        addAnswerButtonDesign = QPixmap("addAnswerButtonDesign.png")
        addAnswerButtonIcon.addPixmap(addAnswerButtonDesign)

        self.widgets['question'].setStyleSheet("font-size: 18px; background: '#ffffff'")
        self.widgets['question'].setPlaceholderText("Enter question")
        self.widgets['question'].editingFinished.connect(self.on_add_question)
        
        self.widgets['time'].setStyleSheet("font-size: 14px; background: '#ffffff'")
        self.widgets['time'].setPlaceholderText("Enter time")
        self.widgets['time'].setValidator(QIntValidator(1, 600))
        self.widgets['time'].editingFinished.connect(self.on_add_time)
        self.widgets['time'].setMaximumWidth(70)

        self.widgets['addAnswer'].clicked.connect(self.on_add_answer)
        self.widgets['addAnswer'].setCursor(QCursor(Qt.PointingHandCursor))
        self.widgets['addAnswer'].setStyleSheet("background: '#ffffff'")
        self.widgets['addAnswer'].setIcon(addAnswerButtonIcon)
        self.widgets['addAnswer'].setIconSize(addAnswerButtonDesign.rect().size())

        self.widgets['answers'].setExclusive(False)

        questionWithTimeLayout = QHBoxLayout()
        questionWithTimeLayout.addWidget(self.widgets['question'])
        questionWithTimeLayout.addWidget(self.widgets['time'])

        self.formLayout = QFormLayout()
        self.formLayout.addRow(questionWithTimeLayout)
        self.formLayout.addRow(self.widgets['addAnswer'])

        layout = QVBoxLayout()
        layout.addLayout(self.formLayout)
        self.setLayout(layout)

    def on_add_question(self):
        self.question.questionText = self.widgets['question'].text()

    def on_add_time(self):
        self.question.questionTime = self.widgets['time'].text()

    def on_add_answer(self):
        self.answerLineEdit = QLineEdit()
        self.answerLineEdit.setPlaceholderText("Enter answer")
        self.answerLineEdit.setStyleSheet("font-size: 16px; background: '#ffffff';")

        confirmAnswerButtonIcon = QIcon()
        confirmAnswerButtonDesign = QPixmap("confirmAnswerButtonDesign.png")
        confirmAnswerButtonIcon.addPixmap(confirmAnswerButtonDesign)

        confirmAnswerButton = QPushButton()
        confirmAnswerButton.clicked.connect(self.confirm_answer)
        confirmAnswerButton.setCursor(QCursor(Qt.PointingHandCursor))
        confirmAnswerButton.setStyleSheet("background: '#ffffff'")
        confirmAnswerButton.setFixedSize(170,50)
        confirmAnswerButton.setIcon(confirmAnswerButtonIcon)
        confirmAnswerButton.setIconSize(confirmAnswerButtonDesign.rect().size())
        

        formLayout = QFormLayout()
        formLayout.addRow(self.answerLineEdit)
        formLayout.addRow(confirmAnswerButton)
    
        self.createAnswerDialog = QDialog()
        self.createAnswerDialog.setStyleSheet("background: #6fce6f;")
        self.createAnswerDialog.setWindowTitle("Create answer")
        self.createAnswerDialog.setFixedSize(600,100)
        self.createAnswerDialog.setWindowModality(Qt.ApplicationModal)
        self.createAnswerDialog.setLayout(formLayout)
        self.createAnswerDialog.exec()

        if self.createAnswerDialog.result() == QDialog.Accepted:
            buttonToAdd = QRadioButton(self.answerLineEdit.text())
            buttonToAdd.setStyleSheet("font-size: 14px")
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
        
        if self.question.questionText and self.answers and correctAnswersIds and self.question.questionTime:
            idTest = database.insert_test(test)
            idQuestion = database.insert_question(self.question, idTest)
            
            for i, answer in enumerate(self.answers):
                if i in correctAnswersIds:
                    answer.isCorrect = True
                database.insert_answer(answer, idQuestion)

            database.commit()
            return True

        return False

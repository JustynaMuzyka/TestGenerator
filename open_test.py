from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor
from PySide6.QtWidgets import (
    QMainWindow,
    QInputDialog,
    QMessageBox,
    QWidget,
    QLabel, 
    QGridLayout,
    QStackedWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton
    )
from open_test_single_choice_question_widget import OpenTestSingleChoiceQuestionWidget
from open_test_multiple_choice_question_widget import OpenTestMultipleChoiceQuestionWidget
from open_test_open_question_widget import OpenTestOpenQuestionWidget
from database import database, Test
from database import Question

class OpenTestWidget(QWidget):

    def __init__(self):
        super().__init__()
        
        self.questionsStackedWidget = QStackedWidget()
        buttonsBottomLayout = self.prepare_buttons_bottom_layout()
        widgetLayout = QVBoxLayout()
        widgetLayout.addWidget(self.questionsStackedWidget)
        widgetLayout.addLayout(buttonsBottomLayout)
        self.setLayout(widgetLayout)

    def prepare_buttons_bottom_layout(self):
        self.buttons = {
            'next' : QPushButton("Next"),
            'finish' : QPushButton("Finish")
            }

        self.buttons['next'].clicked.connect(self.on_next)
        self.buttons['next'].setCursor(QCursor(Qt.PointingHandCursor))
        self.buttons['next'].setStyleSheet(
            "*{border: 3px solid '#0E9110';"+
            "font-size: 25px}"+
            "*:hover{background: '#0E9110';}"
            )

        self.buttons['finish'].clicked.connect(self.on_finish)
        self.buttons['finish'].setCursor(QCursor(Qt.PointingHandCursor))
        self.buttons['finish'].setStyleSheet(
            "*{border: 3px solid '#0E9110';"+
            "font-size: 25px}"+
            "*:hover{background: '#0E9110';}"
            )

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignBottom)
        layout.addWidget(self.buttons['next'])
        layout.addWidget(self.buttons['finish'])
        return layout       


    def choose_test(self):
        result = self.try_choose_test()

        while result < 0:
            result = self.try_choose_test()

        if result == 0:
            return False
        
        return True

    def try_choose_test(self):
        testNames = database.query_test_names()
        testName, okPressed = QInputDialog.getItem(self, "Test", "Write name of your test:", testNames)

        if okPressed:
            if testName in testNames:
                self.test = Test(testName)
                filepath = testName + ".txt"
                self.file = open(filepath, "w")
                self.results = database.query_questions(self.test)
                self.currentQuestion = 0
                self.check_question_type()
                return 1
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("background: #6fce6f;")
            msg.setInformativeText("Test doesn't exists in database!")
            msg.setWindowTitle("Error")
            msg.exec()
            return -1
        else:
            return 0

    def check_question_type(self):
        if self.currentQuestion < len(self.results):
            question = self.results[self.currentQuestion]['question']

            if question.questionType == 'SINGLE':
                self.current_single_choice_question()
                self.currentQuestion +=1
            if question.questionType == 'MULTIPLE':
                self.current_multiple_choice_question()
                self.currentQuestion +=1
            if question.questionType == 'OPEN':
                self.current_open_question()
                self.currentQuestion +=1
        else:
            self.on_finish()

    def on_next(self):
        if self.questionsStackedWidget.count() == 1:
            widgetToDelete = self.questionsStackedWidget.currentWidget()
            if widgetToDelete.on_next(self.file):
                self.questionsStackedWidget.removeWidget(widgetToDelete)
                self.check_question_type()
                
    def current_single_choice_question(self):
        self.currentQuestionWidget = OpenTestSingleChoiceQuestionWidget(self.results[self.currentQuestion])
        self.questionsStackedWidget.addWidget(self.currentQuestionWidget)
        self.questionsStackedWidget.setCurrentIndex(1)

    def current_multiple_choice_question(self):
        self.currentQuestionWidget = OpenTestMultipleChoiceQuestionWidget(self.results[self.currentQuestion])
        self.questionsStackedWidget.addWidget(self.currentQuestionWidget)
        self.questionsStackedWidget.setCurrentIndex(1)

    def current_open_question(self):
        self.currentQuestionWidget = OpenTestOpenQuestionWidget(self.results[self.currentQuestion])
        self.questionsStackedWidget.addWidget(self.currentQuestionWidget)
        self.questionsStackedWidget.setCurrentIndex(1)

    onFinishSignalOT = Signal()
    def on_finish(self):
        self.onFinishSignalOT.emit()

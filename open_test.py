from time import strftime, gmtime
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QCursor, QPixmap, QIcon
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
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_timeout)
        
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.timeRemainingLabel = QLabel()
        self.timeRemainingLabel.setFont(font)

        questionAndTimerLayout = QHBoxLayout()
        questionAndTimerLayout.addWidget(self.questionsStackedWidget)
        questionAndTimerLayout.addWidget(self.timeRemainingLabel)
        questionAndTimerLayout.setAlignment(self.timeRemainingLabel, Qt.AlignTop)

        buttonsBottomLayout = self.prepare_buttons_bottom_layout()

        widgetLayout = QVBoxLayout()
        widgetLayout.addLayout(questionAndTimerLayout)
        widgetLayout.addLayout(buttonsBottomLayout)
        self.setLayout(widgetLayout)

    def prepare_buttons_bottom_layout(self):
        self.buttons = {
            'next' : QPushButton(),
            'finish' : QPushButton()
            }
        nextButtonIcon = QIcon()
        finishButtonIcon = QIcon()

        nextButtonDesign = QPixmap("nextButtonDesign.png")
        finishButtonDesign = QPixmap("finishButtonDesign.png")

        nextButtonIcon.addPixmap(nextButtonDesign)
        finishButtonIcon.addPixmap(finishButtonDesign)

        self.buttons['next'].clicked.connect(self.on_next)
        self.buttons['next'].setCursor(QCursor(Qt.PointingHandCursor))
        self.buttons['next'].setStyleSheet("background: '#ffffff'")
        self.buttons['next'].setIcon(nextButtonIcon)
        self.buttons['next'].setIconSize(nextButtonDesign.rect().size())
        

        self.buttons['finish'].clicked.connect(self.on_finish)
        self.buttons['finish'].setCursor(QCursor(Qt.PointingHandCursor))
        self.buttons['finish'].setStyleSheet("background: '#ffffff'")
        self.buttons['finish'].setIcon(finishButtonIcon)
        self.buttons['finish'].setIconSize(finishButtonDesign.rect().size())


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
            self.isTimeout = False
            self.remainingTime = question.questionTime
            self.timer.start(question.questionTime)

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

    def on_timeout(self):
        self.remainingTime -= self.timer.remainingTime() / 1000.0
        timeString = strftime('%M:%S', gmtime(self.remainingTime))
        self.timeRemainingLabel.setText(timeString)

        if timeString == '00:00':
            self.isTimeout = True
            self.on_next()

    def on_next(self):
        if self.questionsStackedWidget.count() == 1:
            widgetToDelete = self.questionsStackedWidget.currentWidget()
            if widgetToDelete.on_next(self.file, self.isTimeout):
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

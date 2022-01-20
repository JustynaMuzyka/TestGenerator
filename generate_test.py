from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor, QPixmap, QIcon
from PySide6.QtWidgets import (
    QInputDialog,
    QLineEdit,
    QMessageBox,
    QStackedWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton
    )
from question_types_widget import QuestionTypesWidget
from single_choice_question_widget import SingleChoiceQuestionWidget
from multiple_choice_question_widget import MultipleChoiceQuestionWidget
from open_question_widget import OpenQuestionWidget
from database import database, Test

class GenerateTestWidget(QWidget):
    
    def __init__(self):
        super().__init__()

        questionTypesWidget = QuestionTypesWidget()
        questionTypesWidget.onSingleChoiceQuestion.connect(self.on_single_choice_question)
        questionTypesWidget.onMultipleChoiceQuestion.connect(self.on_multiple_choice_question)
        questionTypesWidget.onOpenQuestion.connect(self.on_open_question)

        self.questionsStackedWidget = QStackedWidget()
        self.questionsStackedWidget.addWidget(questionTypesWidget)

        buttonsBottomLayout = self.prepare_buttons_bottom_layout()

        widgetLayout = QVBoxLayout()
        widgetLayout.addWidget(self.questionsStackedWidget)
        widgetLayout.addLayout(buttonsBottomLayout)
        self.setLayout(widgetLayout)

    def prepare_buttons_bottom_layout(self):

        self.buttons = {
            'confirm' : QPushButton(),
            'finish' : QPushButton()
            }
        confirmButtonIcon = QIcon()
        finishButtonIcon = QIcon()

        confirmButtonDesign = QPixmap("confirmButtonDesign.png")
        finishButtonDesign = QPixmap("finishButtonDesign.png")

        confirmButtonIcon.addPixmap(confirmButtonDesign)
        finishButtonIcon.addPixmap(finishButtonDesign)

        self.buttons['confirm'].clicked.connect(self.on_next)
        self.buttons['confirm'].setCursor(QCursor(Qt.PointingHandCursor))
        self.buttons['confirm'].setStyleSheet("background: '#ffffff'")
        self.buttons['confirm'].setIcon(confirmButtonIcon)
        self.buttons['confirm'].setIconSize(confirmButtonDesign.rect().size())
        

        self.buttons['finish'].clicked.connect(self.on_finish)
        self.buttons['finish'].setCursor(QCursor(Qt.PointingHandCursor))
        self.buttons['finish'].setStyleSheet("background: '#ffffff'")
        self.buttons['finish'].setIcon(finishButtonIcon)
        self.buttons['finish'].setIconSize(finishButtonDesign.rect().size())

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignBottom)
        layout.addWidget(self.buttons['confirm'])
        layout.addWidget(self.buttons['finish'])
        return layout

    def create_test(self):
        result = self.try_insert_test()

        while result < 0:
            self.on_finish()
            result = self.try_insert_test()

        if result == 0:
            self.on_finish()
            return False

        return True

    def try_insert_test(self):
        testNames = database.query_test_names()
        testName, okPressed = QInputDialog.getText(self, "Test", "Write name of your test:", QLineEdit.Normal)


        if okPressed:
            if testName and testName not in testNames:
                self.test = Test(testName)
                return 1

            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setStyleSheet("background: #6fce6f;")

            if not testName:
                msg.setInformativeText("Test name can not be empty!")
            elif testName in testNames:
                msg.setInformativeText("Test name already exists!")

            msg.setWindowTitle("Error")
            msg.exec()
            return -1
        else:
            return 0

    def on_next(self):
        if self.questionsStackedWidget.count() == 2:
            widgetToDelete = self.questionsStackedWidget.currentWidget()
            if widgetToDelete.on_next(self.test):
                self.questionsStackedWidget.removeWidget(widgetToDelete)
       
    def on_single_choice_question(self):
        singleChoiceQuestionWidget = SingleChoiceQuestionWidget()
        self.questionsStackedWidget.addWidget(singleChoiceQuestionWidget)
        self.questionsStackedWidget.setCurrentIndex(1)

    def on_multiple_choice_question(self):
        multipleChoiceQuestionWidget = MultipleChoiceQuestionWidget()
        self.questionsStackedWidget.addWidget(multipleChoiceQuestionWidget)
        self.questionsStackedWidget.setCurrentIndex(1)

    def on_open_question(self):
        openQuestionWidget = OpenQuestionWidget()
        self.questionsStackedWidget.addWidget(openQuestionWidget)
        self.questionsStackedWidget.setCurrentIndex(1)

    onFinishSignalGT = Signal()
    def on_finish(self):
        self.onFinishSignalGT.emit()

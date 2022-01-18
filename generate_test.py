from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
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
from database import database, Test

class GenerateTestWidget(QWidget):
    
    def __init__(self):
        super().__init__()

        questionTypesWidget = QuestionTypesWidget()
        

        self.questionsStackedWidget = QStackedWidget()
        self.questionsStackedWidget.addWidget(questionTypesWidget)
        
        buttonsBottomLayout = self.prepare_buttons_bottom_layout()

        widgetLayout = QVBoxLayout()
        widgetLayout.addWidget(self.questionsStackedWidget)
        widgetLayout.addLayout(buttonsBottomLayout)
        self.setLayout(widgetLayout)

    def prepare_buttons_bottom_layout(self):
        self.buttons = {
            'confirm' : QPushButton("Confirm"),
            'finish' : QPushButton("Finish")
            }

        self.buttons['confirm'].clicked.connect(self.on_next)
        self.buttons['confirm'].setCursor(QCursor(Qt.PointingHandCursor))
        self.buttons['confirm'].setStyleSheet(
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
        layout.addWidget(self.buttons['confirm'])
        layout.addWidget(self.buttons['finish'])
        return layout

    def create_test(self):
        result = self.try_insert_test()

        while result < 0:
            result = self.try_insert_test()

        if result == 0:
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

    onFinishSignal = Signal()
    def on_finish(self):
        self.onFinishSignal.emit()

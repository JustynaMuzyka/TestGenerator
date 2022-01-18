from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QPushButton
    )

class QuestionTypesWidget(QWidget):
    onSingleChoiceQuestion = Signal()
    def on_single_choice_question(self):
        self.onSingleChoiceQuestion.emit()

    onMultipleChoiceQuestion = Signal()
    def on_multiple_choice_question(self):
        self.onMultipleChoiceQuestion.emit()

    onOpenQuestion = Signal()
    def on_open_question(self):
        self.onOpenQuestion.emit()

    def __init__(self):
        super().__init__()

        questionTypesButtons = {
            'singleChoice' : QPushButton("Single choice question"),
            'multipleChoice' : QPushButton("Multiple choice question"),
            'openQuestion' : QPushButton("Open question")
            }

        questionTypesButtons['singleChoice'].clicked.connect(self.on_single_choice_question)
        questionTypesButtons['multipleChoice'].clicked.connect(self.on_multiple_choice_question)
        questionTypesButtons['openQuestion'].clicked.connect(self.on_open_question)

        layout = QFormLayout()
        for button in questionTypesButtons.values():
            button.setCursor(QCursor(Qt.PointingHandCursor))
            button.setStyleSheet("font-size: 20px; background: '#14A817'")
            layout.addRow(button)
        
        self.setLayout(layout)


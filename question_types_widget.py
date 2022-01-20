from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCursor, QPixmap, QIcon
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
            'singleChoice' : QPushButton(),
            'multipleChoice' : QPushButton(),
            'openQuestion' : QPushButton()
            }
        singleChoiceButtonIcon = QIcon()
        multipleChoiceButtonIcon = QIcon()
        openQuestionButtonIcon = QIcon()

        singleChoiceButtonDesign = QPixmap("singleChoiceButtonDesign.png")
        multipleChoiceButtonDesign = QPixmap("multipleChoiceButtonDesign.png")
        openQuestionButtonDesign = QPixmap("openQuestionButtonDesign.png")

        singleChoiceButtonIcon.addPixmap(singleChoiceButtonDesign)
        multipleChoiceButtonIcon.addPixmap(multipleChoiceButtonDesign)
        openQuestionButtonIcon.addPixmap(openQuestionButtonDesign)

        questionTypesButtons['singleChoice'].clicked.connect(self.on_single_choice_question)
        questionTypesButtons['singleChoice'].setCursor(QCursor(Qt.PointingHandCursor))
        questionTypesButtons['singleChoice'].setStyleSheet("background: '#ffffff'")
        questionTypesButtons['singleChoice'].setIcon(singleChoiceButtonIcon)
        questionTypesButtons['singleChoice'].setIconSize(singleChoiceButtonDesign.rect().size())

        questionTypesButtons['multipleChoice'].clicked.connect(self.on_multiple_choice_question)
        questionTypesButtons['multipleChoice'].setCursor(QCursor(Qt.PointingHandCursor))
        questionTypesButtons['multipleChoice'].setStyleSheet("background: '#ffffff'")
        questionTypesButtons['multipleChoice'].setIcon(multipleChoiceButtonIcon)
        questionTypesButtons['multipleChoice'].setIconSize(multipleChoiceButtonDesign.rect().size())

        questionTypesButtons['openQuestion'].clicked.connect(self.on_open_question)
        questionTypesButtons['openQuestion'].setCursor(QCursor(Qt.PointingHandCursor))
        questionTypesButtons['openQuestion'].setStyleSheet("background: '#ffffff'")
        questionTypesButtons['openQuestion'].setIcon(openQuestionButtonIcon)
        questionTypesButtons['openQuestion'].setIconSize(openQuestionButtonDesign.rect().size())

        layout = QFormLayout()
        layout.addRow(questionTypesButtons['singleChoice'])
        layout.addRow(questionTypesButtons['multipleChoice'])
        layout.addRow(questionTypesButtons['openQuestion'])
        
        self.setLayout(layout)


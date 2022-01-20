from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor, QPixmap, QIcon
from PySide6.QtWidgets import (
    QWidget,
    QLabel, 
    QGridLayout,
    QPushButton
    )

class MainMenuWidget(QWidget):
    onGenerateTestSignal = Signal()
    def on_generate_test(self):
        self.onGenerateTestSignal.emit()

    onOpenTestSignal = Signal()
    def on_open_test(self):
        self.onOpenTestSignal.emit()

    def __init__(self):
        super().__init__()

        widgets = {
            'title' : QLabel(),
            'generateTest' : QPushButton(),
            'openTest' : QPushButton()
            }
        generateTestButtonIcon = QIcon()
        openTestButtonIcon = QIcon()

        applicationLogoDesign = QPixmap("logo.png")
        generateTestButtonDesign = QPixmap("generateTestButton.png")
        openTestButtonDesign = QPixmap("openTestButton.png")

        generateTestButtonIcon.addPixmap(generateTestButtonDesign)
        openTestButtonIcon.addPixmap(openTestButtonDesign)

        widgets['title'].setPixmap(applicationLogoDesign)
        widgets['title'].setAlignment(Qt.AlignCenter)

        widgets['generateTest'].clicked.connect(self.on_generate_test)
        widgets['generateTest'].setCursor(QCursor(Qt.PointingHandCursor))
        widgets['generateTest'].setStyleSheet("background: '#ffffff'")
        widgets['generateTest'].setIcon(generateTestButtonIcon)
        widgets['generateTest'].setIconSize(generateTestButtonDesign.rect().size())
        
        widgets['openTest'].clicked.connect(self.on_open_test)
        widgets['openTest'].setCursor(QCursor(Qt.PointingHandCursor))
        widgets['openTest'].setStyleSheet("background: '#ffffff'")
        widgets['openTest'].setIcon(openTestButtonIcon)
        widgets['openTest'].setIconSize(openTestButtonDesign.rect().size())
        
        layout = QGridLayout()
        layout.addWidget(widgets['title'], 0, 1)
        layout.addWidget(widgets['generateTest'], 1, 0)
        layout.addWidget(widgets['openTest'], 1, 2)
        self.setLayout(layout)



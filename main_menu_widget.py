from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QCursor
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
            'generateTest' : QPushButton("Generate Test"),
            'openTest' : QPushButton("Open Test")
            }

        font = QFont()
        font.setPointSize(28)
        font.setBold(True)
        
        widgets['title'].setText("Welcome to\n Test Generator!")
        widgets['title'].setFont(font)
        widgets['title'].setAlignment(Qt.AlignCenter)
        widgets['title'].setStyleSheet("margin: 15px 50px")
        
        widgets['generateTest'].clicked.connect(self.on_generate_test)
        widgets['generateTest'].setFixedWidth(250)
        widgets['generateTest'].setCursor(QCursor(Qt.PointingHandCursor))
        widgets['generateTest'].setStyleSheet(
            "*{border: 2px solid '#49aa2e';"+
            "font-size: 25px;"+
            "margin: 20px 10px}"+
            "*:hover{background: '#49aa2e';}"
            )
        
        widgets['openTest'].clicked.connect(self.on_open_test)
        widgets['openTest'].setFixedWidth(250)
        widgets['openTest'].setCursor(QCursor(Qt.PointingHandCursor))
        widgets['openTest'].setStyleSheet(
            "*{border: 2px solid '#49aa2e';"+
            "font-size: 25px;"+
            "margin: 20px 10px}"+
            "*:hover{background: '#49aa2e';}"
            )
        
        layout = QGridLayout()
        layout.addWidget(widgets['title'], 0, 1)
        layout.addWidget(widgets['generateTest'], 1, 0)
        layout.addWidget(widgets['openTest'], 1, 2)
        self.setLayout(layout)



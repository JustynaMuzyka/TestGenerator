from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QLayout, QHBoxLayout, QInputDialog, QLineEdit
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
import sys

widgets = {
    "title": [],
    "button1": [],
    "button2": [],
    "button3": [],
    "button4": [],
    "a1": [],
    "q": [],
    }

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tests Generator")
        self.setFixedWidth(1300)
        self.setStyleSheet("background: #6fce6f;")
        self.setLayout(QtWidgets.QGridLayout())
        self.start_scr()

    def start_scr(self):
        f = QFont()
        f.setPointSize(28)
        f.setBold(True)
        f.setWeight(75)

        #title
        title = QLabel()
        title.setText("Welcome to\n Tests Generator!")
        title.setFont(f)
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("margin: 15px 50px")


        #button1
        self.button1 = QPushButton("Generate Test", clicked = generateTest)
        self.button1.setStyleSheet(
            "*{border: 6px solid '#b99545';"+
            "font-size: 50px;"+
            "margin: 20px 10px}"+
            "*:hover{background: '#b99545';}"
            )
        self.button1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    

        #button2
        self.button2 = QPushButton("Open Test")
        self.button2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button2.setStyleSheet(
            "*{border: 6px solid '#b99545';"+
            "font-size: 50px;"+
            "margin: 20px 10px}"+
            "*:hover{background: '#b99545';}"
            )

        
        widgets["title"].append(title)
        widgets["button1"].append(self.button1)
        widgets["button2"].append(self.button2)

        self.layout().addWidget(widgets["title"][-1], 0, 1)
        self.layout().addWidget(widgets["button1"][-1], 1, 0)
        self.layout().addWidget(widgets["button2"][-1], 1, 2)


class QuestionWindow(MainWindow):
    
    def __init__(self):
        super().__init__()

    def setButtons(self):
        self.button3 = QPushButton("Next", clicked = createTest)
        self.button3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button3.setStyleSheet(
            "*{border: 6px solid '#b99545';"+
            "font-size: 25px;"+
            "margin: 15px 10px}"+
            "*:hover{background: '#b99545';}"
            )
        self.button3.setFixedWidth(200)

        self.button4 = QPushButton("Finish", clicked = finishGeneration)
        self.button4.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button4.setStyleSheet(
            "*{border: 6px solid '#b99545';"+
            "font-size: 25px;"+
            "margin: 15px 10px}"+
            "*:hover{background: '#b99545';}"
            )

        widgets["button3"].append(self.button3)
        widgets["button4"].append(self.button4)

        self.layout().addWidget(widgets["button3"][-1], 8, 1)
        self.layout().addWidget(widgets["button4"][-1], 9, 1)


    def getQuestion(self):
        text, okPressed = QInputDialog.getText(self, "Question","Input a question:", QLineEdit.Normal, "question")
        if okPressed and text != '':
            self.question = QLabel()
            self.question.setText(text)
            f = QFont()
            f.setPointSize(28)
            f.setBold(True)
            f.setWeight(75)
            self.question.setFont(f)
            widgets["q"].append(self.question)  
            self.layout().addWidget(widgets["q"][-1], 0, 0)

            
            num,ok = QInputDialog.getInt(self,"Specify number od answers","Enter a number")
            row = 1
            if ok:
                for i in range(0, num):
                    text, okPressed = QInputDialog.getText(self, "Answer","Input answer:", QLineEdit.Normal, "")
                    if okPressed and text != '':
                        self.b1 = QLabel(text)
                        widgets["a1"].append(self.b1)
                        self.layout().addWidget(widgets["a1"][-1], row, 0)
                        row += 1
         


def clearWidgets():
    for widget in widgets:
        if widgets[widget] != []:
            for i in range(0, len(widgets[widget])):
                widgets[widget][i].hide()
        for i in range(0, len(widgets[widget])):
            widgets[widget].pop()

def generateTest():
    

    text, okPressed = QInputDialog.getText(win2, "Test","Write name of your test:", QLineEdit.Normal, "test1")
    if okPressed and text != '':
        clearWidgets()
        win.close()
        win2.show()
        win2.setButtons()
        win2.setWindowTitle(text) 
        createTest()


def createTest():
    clearWidgets()
    win2.show()
    win2.setButtons()
    win2.getQuestion()

def finishGeneration():
    win2.close()
    win.show()
    win.start_scr()

app = QApplication([])
win = MainWindow()
win2 = QuestionWindow()
win.show()
app.exec_()






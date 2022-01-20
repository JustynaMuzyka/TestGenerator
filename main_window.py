from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    )

from database import database
from main_menu_widget import MainMenuWidget
from generate_test import GenerateTestWidget
from open_test import OpenTestWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Test Generator")
        self.setFixedSize(QSize(1024, 576))
        self.setStyleSheet("background: #6fce6f;")
        
        self.mainMenuWidget = MainMenuWidget()
        self.mainMenuWidget.onGenerateTestSignal.connect(self.generate_test_slot)
        self.mainMenuWidget.onOpenTestSignal.connect(self.open_test_slot)
        
        self.centralStackedWidget = QStackedWidget()
        self.centralStackedWidget.addWidget(self.mainMenuWidget)
        
        layout = QVBoxLayout()
        layout.addWidget(self.centralStackedWidget)
        self.setLayout(layout)

        self.setCentralWidget(self.centralStackedWidget)

    def return_to_main_menu_slot(self):
        for i in range(self.centralStackedWidget.count() - 1, 0, -1):
            widgetToDelete = self.centralStackedWidget.widget(i)
            self.centralStackedWidget.removeWidget(widgetToDelete)

    def generate_test_slot(self):
        generateTestWidget = GenerateTestWidget()
        generateTestWidget.onFinishSignalGT.connect(self.return_to_main_menu_slot)
        self.centralStackedWidget.addWidget(generateTestWidget)
        
        if self.centralWidget().widget(1).create_test():
            self.centralWidget().setCurrentIndex(1)
        else:
            self.centralWidget().removeWidget(generateTestWidget)

    def open_test_slot(self):
        openTestWidget = OpenTestWidget()
        openTestWidget.onFinishSignalOT.connect(self.return_to_main_menu_slot)
        self.centralStackedWidget.addWidget(openTestWidget)

        if self.centralWidget().widget(1).choose_test():
            self.centralWidget().setCurrentIndex(1)
        else:
            self.centralWidget().removeWidget(openTestWidget)

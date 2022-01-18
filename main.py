from PySide6.QtWidgets import QApplication
from main_window import MainWindow

def main():
    app = QApplication([])
    
    mainWindow = MainWindow()
    mainWindow.show()

    app.exec()

if __name__ == '__main__':
	main()





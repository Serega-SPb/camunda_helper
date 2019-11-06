import sys

from PyQt5.QtWidgets import QApplication

from ui.main_ui_logic import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()

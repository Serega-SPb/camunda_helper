import sys

from PyQt5.QtWidgets import QApplication

from ui.model import MainModel as Model
from ui.view import MainView as View
from ui.controller import MainController as Controller
from ui.main_ui_logic import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    model = Model()
    controller = Controller(model)
    view = View(model, controller)
    view.show()

    # window = MainWindow()
    # window.show()
    app.exec_()

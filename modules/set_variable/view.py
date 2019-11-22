from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

# from .view_ui import Ui_Form


class SVView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller

        # self.ui = Ui_Form()
        # self.ui.setupUi(self)

        self.connect_widgets()
        self.connect_model_signals()

    def connect_widgets(self):
        pass

    def connect_model_signals(self):
        pass

    # TODO Slots

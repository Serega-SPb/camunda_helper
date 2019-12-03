from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from .view_ui import Ui_Form


class MTView(QWidget):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)

        self.model = model
        self.controller = controller

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.connect_widgets()
        self.connect_model_signals()

    def connect_widgets(self):
        self.ui.closeTaskChbx.toggled['bool'].connect(self.controller.is_close_change)
        self.ui.startTaskChbx.toggled['bool'].connect(self.controller.is_start_change)
        self.ui.closeTaskTxb.textChanged.connect(self.controller.close_change)
        self.ui.startTaskTxb.textChanged.connect(self.controller.start_change)
        self.ui.transpositionBtn.clicked.connect(self.controller.transposition)

    def connect_model_signals(self):
        self.model.is_close_changed.connect(self.on_is_close_changed)
        self.model.is_start_changed.connect(self.on_is_start_changed)
        self.model.close_changed.connect(self.on_close_changed)
        self.model.start_changed.connect(self.on_start_changed)

    @pyqtSlot(bool)
    def on_is_close_changed(self, value):
        self.ui.closeTaskChbx.setChecked(value)

    @pyqtSlot(str)
    def on_close_changed(self, value):
        self.ui.closeTaskTxb.setText(value)

    @pyqtSlot(bool)
    def on_is_start_changed(self, value):
        self.ui.startTaskChbx.setChecked(value)

    @pyqtSlot(str)
    def on_start_changed(self, value):
        self.ui.startTaskTxb.setText(value)

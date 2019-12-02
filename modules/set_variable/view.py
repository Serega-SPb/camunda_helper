from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget

from .view_ui import Ui_Form


class SVView(QWidget):

    STATUS = {
        True: ('VALID', "color:rgb(255, 255, 255);\n background-color:rgb(0, 170, 0)"),
        False: ('INVALID', "color:rgb(255, 255, 255);\n background-color:rgb(170, 0, 0)"),
    }

    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.connect_widgets()
        self.connect_model_signals()

        self.on_valid_status_changed(False)

    def connect_widgets(self):
        self.ui.nameVarTxb.textChanged.connect(self.controller.name_var_change)
        self.ui.typeVarCmb.currentTextChanged.connect(self.controller.type_var_change)
        self.ui.valueVarPte.textChanged.connect(self.value_var_change)

    def connect_model_signals(self):
        self.model.name_var_changed.connect(self.on_name_var_changed)
        self.model.type_var_changed.connect(self.on_type_var_changed)
        self.model.value_var_changed.connect(self.on_value_var_changed)
        self.model.value_is_valid_changed.connect(self.on_valid_status_changed)

    @pyqtSlot(str)
    def on_name_var_changed(self, value):
        self.ui.nameVarTxb.setText(value)

    @pyqtSlot(str)
    def on_type_var_changed(self, value):
        self.ui.typeVarCmb.setCurrentText(value)

    @pyqtSlot(str)
    def on_value_var_changed(self, value):
        if self.ui.valueVarPte.toPlainText() != value:
            self.ui.valueVarPte.setPlainText(value)

    @pyqtSlot(bool)
    def on_valid_status_changed(self, value):
        txt, style = self.STATUS[value]
        self.ui.validStatusLbl.setText(txt)
        self.ui.validStatusLbl.setStyleSheet(style)

    def value_var_change(self):
        self.controller.value_var_change(self.ui.valueVarPte.toPlainText())
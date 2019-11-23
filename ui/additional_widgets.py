import base64
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDialog, QGridLayout, \
                            QHBoxLayout, QWidgetAction, QFormLayout, \
                            QLabel, QLineEdit, QPushButton, QCheckBox


class ConfigWidget(QWidget):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.ui()
        self.config.subscribe('name', self.set_lbl)
        self.config.subscribe('host', self.set_lbl)
        self.set_lbl()
        self.configLbl.destroyed.connect(lambda: self.unsubscribe())

    def unsubscribe(self):
        self.config.unsubscribe('name', self.set_lbl)
        self.config.unsubscribe('host', self.set_lbl)

    def ui(self):
        grid = QGridLayout(self)
        self.setLayout(grid)
        self.configLbl = QLabel(self)
        grid.addWidget(self.configLbl)

    def set_lbl(self, *args):
        self.configLbl.setText(str(self.config))


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui()
        self.confirm = False

    def ui(self):

        self.resize(250, 125)
        self.setFixedSize(self.size())
        self.setWindowTitle('Login')
        self.setModal(True)

        grid = QGridLayout(self)
        self.setLayout(grid)
        hbox = QHBoxLayout(self)

        self.loginLbl = QLabel()
        self.loginLbl.setText('Login')
        self.passLbl = QLabel()
        self.passLbl.setText('Password')

        self.loginTxb = QLineEdit()
        self.passTxb = QLineEdit()
        self.passTxb.setEchoMode(QLineEdit.Password)

        grid.addWidget(self.loginLbl, 0, 0)
        grid.addWidget(self.passLbl, 1, 0)
        grid.addWidget(self.loginTxb, 0, 1)
        grid.addWidget(self.passTxb, 1, 1)

        self.okBtn = QPushButton()
        self.okBtn.setText('Login')
        self.okBtn.clicked.connect(self.ok_btn_click)
        self.cancelBtn = QPushButton()
        self.cancelBtn.setText('Cancel')
        self.cancelBtn.clicked.connect(self.cancel_btn_click)

        hbox.addWidget(self.okBtn)
        hbox.addWidget(self.cancelBtn)
        grid.addLayout(hbox, 3, 0, 1, 2)

    def __save_login_pass(self):
        login_pass = f'{self.loginTxb.text()}:{self.passTxb.text()}'
        with open('login.txt', 'wb') as file:
            file.write(base64.b64encode(login_pass.encode()))

    def ok_btn_click(self):
        self.__save_login_pass()
        self.confirm = True
        self.close()

    def cancel_btn_click(self):
        self.confirm = False
        self.close()


class InputMenuAction(QWidget):

    valueChanged = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ui()

    def _ui(self):
        h_box = QHBoxLayout(self)
        h_box.setContentsMargins(0, 3, 0, 3)
        self.setLayout(h_box)

        self.nameLbl = QLabel(self)
        self.valueLE = QLineEdit(self)
        self.valueLE.textChanged.connect(
            lambda v: self.valueChanged.emit(self.label.lower(), v))

        h_box.addWidget(self.nameLbl)
        h_box.addWidget(self.valueLE)

    @property
    def label(self):
        return self.nameLbl.text()

    @label.setter
    def label(self, value):
        self.nameLbl.setText(value.capitalize())

    def get_widget_action(self, parent):
        wid_action = QWidgetAction(parent)
        wid_action.setDefaultWidget(self)
        return wid_action

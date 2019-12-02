from PyQt5.QtCore import QObject, pyqtSignal


class SVModel(QObject):

    name_var_changed = pyqtSignal(str)
    type_var_changed = pyqtSignal(str)
    value_var_changed = pyqtSignal(str)
    value_is_valid_changed = pyqtSignal(bool)
    can_send_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._name_var = ''
        self._type_var = 'json'
        self._value_var = ''
        self._value_is_valid = False

    def __repr__(self):
        return f'<SVModel>(name_var={self.name_var}, type_var={self.type_var}, ' \
               f'value_var={self.value_var}, can_send={self.can_send}, ' \
               f'value_is_valid={self.value_is_valid})'

    @property
    def name_var(self):
        return self._name_var

    @name_var.setter
    def name_var(self, value):
        if value == self._name_var:
            return
        self._name_var = value
        self.name_var_changed.emit(value)
        self.can_send_changed.emit()

    @property
    def type_var(self):
        return self._type_var

    @type_var.setter
    def type_var(self, value):
        if value == self._type_var:
            return
        self._type_var = value
        self.type_var_changed.emit(value)
        self.can_send_changed.emit()

    @property
    def value_var(self):
        return self._value_var

    @value_var.setter
    def value_var(self, value):
        if value == self._value_var:
            return
        self._value_var = value
        self.value_var_changed.emit(value)
        self.can_send_changed.emit()

    @property
    def value_is_valid(self):
        return self._value_is_valid

    @value_is_valid.setter
    def value_is_valid(self, value):
        if value == self._value_is_valid:
            return
        self._value_is_valid = value
        self.value_is_valid_changed.emit(value)
        self.can_send_changed.emit()

    @property
    def can_send(self):
        if not self.value_is_valid:
            return False
        if not self.name_var:
            return False
        if not self.type_var:
            return False
        if not self.value_var:
            return False
        return True

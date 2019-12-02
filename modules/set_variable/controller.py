import json

from PyQt5.QtCore import QObject


class SVController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def name_var_change(self, value):
        self.model.name_var = value

    def type_var_change(self, value):
        self.model.type_var = value

    def value_var_change(self, value):
        self.model.value_var = value
        self.validate_value()

    def validate_value(self):
        var_type = self.model.type_var
        var_value = self.model.value_var
        result = False
        if var_type == 'json':
            try:
                json.loads(var_value)
                result = True
            except Exception:
                result = False
        self.model.value_is_valid = result

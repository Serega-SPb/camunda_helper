from .model import SVModel as Model


class Body:
    TYPE = 'type'
    VALUE = 'value'


class SVRequest:
    METHOD = 'PUT'

    def __init__(self, model: Model):
        self.model = model

    def get_url(self, instance):
        return f'/{instance}/variables/{self.model.name_var}'

    def get_body(self):
        v_type = self.model.type_var
        value = self.model.value_var
        return {Body.TYPE: v_type.capitalize(), Body.VALUE: value}

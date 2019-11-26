from .model import MTModel as Model


class Body:
    INSTRUCTIONS = 'instructions'
    TYPE = 'type'
    START = 'startBeforeActivity'
    CLOSE = 'cancel'
    ACTIVITY_ID = 'activityId'


class MTRequest:
    METHOD = 'POST'
    
    def __init__(self, model: Model):
        self.model = model

    @staticmethod
    def get_url(instance):
        return f'/{instance}/modification'

    def get_body(self):
        instructions = []
        if self.model.is_start:
            instructions.append({Body.TYPE: Body.START, Body.ACTIVITY_ID: self.model.start})
        if self.model.is_close:
            instructions.append({Body.TYPE: Body.CLOSE, Body.ACTIVITY_ID: self.model.close})
        return {Body.INSTRUCTIONS: instructions}

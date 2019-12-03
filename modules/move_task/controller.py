from PyQt5.QtCore import QObject


class MTController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    def is_close_change(self, value):
        self.model.is_close = value

    def close_change(self, value):
        self.model.close = value

    def is_start_change(self, value):
        self.model.is_start = value

    def start_change(self, value):
        self.model.start = value

    def transposition(self):
        model = self.model
        if not model.is_start and not model.is_close:
            return
        model.close, model.start = model.start, model.close
        model.is_close, model.is_start = model.is_start, model.is_close

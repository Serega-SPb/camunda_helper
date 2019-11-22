from PyQt5.QtCore import QObject


class SVController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model

    # TODO Change model handlers (Logic)

from PyQt5.QtCore import QObject, pyqtSignal


class SVModel(QObject):

    # TODO Signals (Events)
    can_send_changed = pyqtSignal()

    def __init__(self):
        super().__init__()

    # TODO Properties

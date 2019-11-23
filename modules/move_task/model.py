from PyQt5.QtCore import QObject, pyqtSignal


class MTModel(QObject):

    is_close_changed = pyqtSignal(bool)
    is_start_changed = pyqtSignal(bool)
    close_changed = pyqtSignal(str)
    start_changed = pyqtSignal(str)
    can_send_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._is_close = False
        self._is_start = False
        self._close = ''
        self._start = ''

    # TODO Properties

    @property
    def is_close(self):
        return self._is_close

    @is_close.setter
    def is_close(self, value):
        self._is_close = value
        self.is_close_changed.emit(value)
        self.can_send_changed.emit()

    @property
    def close(self):
        return self._close

    @close.setter
    def close(self, value):
        self._close = value
        self.close_changed.emit(value)
        self.can_send_changed.emit()

    @property
    def is_start(self):
        return self._is_start

    @is_start.setter
    def is_start(self, value):
        self._is_start = value
        self.is_start_changed.emit(value)
        self.can_send_changed.emit()

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, value):
        self._start = value
        self.start_changed.emit(value)
        self.can_send_changed.emit()

    @property
    def can_send(self):
        if not self.is_close and not self.is_start:
            return False
        if self.is_close and not self.close:
            return False
        if self.is_start and not self.start:
            return False
        return True

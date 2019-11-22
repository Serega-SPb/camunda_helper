import logging
import importlib
from collections import namedtuple

from core import log_config
from core.decorators import try_except_wrapper
from core.metaclasses import Singleton


Module = namedtuple('Module', 'model view controller')


class Manager(metaclass=Singleton):

    MODULE_LIST = ['move_task']

    def __init__(self):
        self.logger = logging.getLogger(log_config.LOGGER_NAME)
        self.__modules = {}
        self.__init_modules()

    def __init_modules(self):
        for m in self.MODULE_LIST:
            self.__import_module(m)

    @try_except_wrapper
    def __import_module(self, module_name):

        mod = importlib.import_module(module_name, package='.')
        if hasattr(mod, 'get_mvc'):
            self.__modules[module_name] = Module(*getattr(mod, 'get_mvc')())

    def get_model_by_name(self, value):
        if value in self.__modules.keys():
            return self.__modules[value].model

    def get_view_by_name(self, value):
        if value in self.__modules.keys():
            return self.__modules[value].view


def test_move_task(manager):
    model = manager.get_model_by_name('move_task')
    model.can_send_changed.connect(lambda: print(str(model)))
    view = manager.get_view_by_name('move_task')
    view.show()


def main():
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    manager = Manager()
    test_move_task(manager)
    app.exec_()


if __name__ == '__main__':
    main()

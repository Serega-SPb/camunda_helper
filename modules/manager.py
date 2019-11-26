import logging
import importlib
import os
from collections import namedtuple

from core import log_config
from core.decorators import try_except_wrapper
from core.metaclasses import Singleton


Module = namedtuple('Module', 'model view controller')


class Manager(metaclass=Singleton):

    MODULE_LIST = ['move_task', 'set_variable']

    def __init__(self):
        self.logger = logging.getLogger(log_config.LOGGER_NAME)
        self.__modules = {}
        self.__request_cl = {}
        self.__init_modules()

    def __init_modules(self):
        for m in self.MODULE_LIST:
            self.__import_module(m)

    @try_except_wrapper
    def __import_module(self, module_name):

        mod = importlib.import_module(module_name, package=os.path.dirname(__file__))
        if hasattr(mod, 'get_mvc'):
            self.__modules[module_name] = Module(*getattr(mod, 'get_mvc')())
        if hasattr(mod, 'get_request_cl'):
            self.__request_cl[module_name] = getattr(mod, 'get_request_cl')

    def get_views(self):
        return {n: m.view for n, m in self.__modules.items()}

    def get_model_by_name(self, value):
        if value in self.__modules.keys():
            return self.__modules[value].model

    def get_view_by_name(self, value):
        if value in self.__modules.keys():
            return self.__modules[value].view

    def create_request(self, module_name):
        if module_name in self.__request_cl.keys():
            model = self.get_model_by_name(module_name)
            return self.__request_cl[module_name](model)

    def update_config_fields(self, config):
        for name, mod in self.__modules.items():
            fields = dict(mod.model.__dict__.items())
            if name not in config.utils:
                config.utils[name] = {f[1:]: v for f, v in fields.items()}
            else:
                for f in fields.keys():
                    p = f[1:]
                    if p not in config.utils[name] or not config.utils[name][p]:
                        config.utils[name][p] = fields[f]

    # TODO
    #  ?
    #  ? def apply_config_views(self, config):


def test_move_task(manager):
    model = manager.get_model_by_name('move_task')
    model.can_send_changed.connect(lambda: print(str(model)))
    view = manager.get_view_by_name('move_task')
    view.show()


def main():
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    manager = Manager()
    views = manager.get_views()
    test_move_task(manager)
    app.exec_()


if __name__ == '__main__':
    main()

import os

from PyQt5.QtCore import QObject, pyqtSignal

from core.config import Config
from modules.manager import Manager as ModuleManager


class MainModel(QObject):
    UI_DIR = os.path.dirname(__file__)
    URLS_FILE = 'urls.yaml'
    CONFIGS_FILE = 'configs.yaml'
    LOGIN_FILE = 'login.txt'

    urls_changed = pyqtSignal(dict)
    configs_changed = pyqtSignal(list)
    config_added = pyqtSignal(Config)
    config_removed = pyqtSignal(Config)

    current_config_changed = pyqtSignal(object)
    login_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._login_pass = None
        self._configs = []
        self._current_module = None
        self._current_config = None
        self._urls = {'auth': '', 'engine': ''}
        self.mod_manager = ModuleManager()

    @property
    def configs(self):
        return self._configs

    @configs.setter
    def configs(self, value):
        self._configs = value
        self.configs_changed.emit(value)

    @property
    def urls(self):
        return self._urls

    @urls.setter
    def urls(self, value):
        self._urls = value
        self.urls_changed.emit(value)

    @property
    def login_pass(self):
        return self._login_pass

    @login_pass.setter
    def login_pass(self, value):
        self._login_pass = value
        self.login_changed.emit(value.split(':')[0] if len(value) > 3 else 'anon')

    @property
    def current_config(self):
        return self._current_config

    @current_config.setter
    def current_config(self, value):
        self._current_config = value
        self.current_config_changed.emit(value)

    @property
    def current_module(self):
        return self._current_module

    @current_module.setter
    def current_module(self, value):
        self._current_module = value

    def add_config(self, value):
        self.configs.append(value)
        self.config_added.emit(value)
        self.configs_changed.emit(self.configs)

    def remove_config(self):
        value = self.current_config
        self.configs.remove(value)
        self.config_removed.emit(value)
        self.configs_changed.emit(self.configs)

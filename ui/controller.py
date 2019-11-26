import base64
import logging
import os

import yaml
from PyQt5.QtCore import QObject

from core import log_config
from core.config import Config
from core.sender import Sender
from core.decorators import try_except_wrapper
from modules.manager import Manager as ModuleManager


def set_field_value(source, field_path, value):
    path = field_path.split('.')
    count = len(path)
    i = 0
    for p in path:
        is_iter = False
        if p.startswith('['):
            is_iter = True
            p = p[1:-1]
            if p.isdigit():
                p = int(p)

        if i == count - 1:
            if is_iter:
                source[p] = value
            else:
                setattr(source, p, value)
            return

        source = source[p] if is_iter else getattr(source, p)
        i += 1


class MainController(QObject):
    def __init__(self, model):
        super().__init__()
        self.model = model
        self.logger = logging.getLogger(log_config.LOGGER_NAME)
        self.mod_manager = ModuleManager()
        self.sender = None
        self.question_method = None

    def load_login(self):
        if not os.path.isfile(self.model.LOGIN_FILE):
            return
        with open(self.model.LOGIN_FILE, 'rb') as file:
            data = file.read()
        self.model.login_pass = base64.b64decode(data).decode()

    @try_except_wrapper
    def load_urls(self):
        if not os.path.isfile(self.model.URLS_FILE):
            return
        with open(self.model.URLS_FILE, 'r', encoding='utf-8') as file:
            data = yaml.load(file, yaml.FullLoader)
        if not data:
            self.logger.warning(f'{self.model.URLS_FILE} is empty')
            return
        self.model.urls = {n: data.get(n, '') for n, u in self.model.urls.items()}
        self.logger.debug('urls loaded')

    @try_except_wrapper
    def save_urls(self):
        with open(self.model.URLS_FILE, 'w', encoding='utf-8') as file:
            yaml.dump(self.model.urls, file, default_flow_style=False)
        self.logger.debug('urls saved')

    def update_url(self, key, value):
        self.model.urls[key] = value

    @try_except_wrapper
    def load_configs(self):
        if not os.path.isfile(self.model.CONFIGS_FILE):
            return
        with open(self.model.CONFIGS_FILE, 'r', encoding='utf-8') as file:
            data = yaml.load(file, yaml.FullLoader)
        if not data:
            self.logger.warning(f'{self.model.CONFIGS_FILE} is empty')
            return

        configs = [Config.from_dict(d) for d in data]
        for conf in configs:
            self.mod_manager.update_config_fields(conf)
        self.model.configs = configs
        self.logger.debug('configs loaded')

    @try_except_wrapper
    def save_configs(self, *args):
        data = [c.get_dict() for c in self.model.configs]
        with open(self.model.CONFIGS_FILE, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False)
        self.logger.debug('configs saved')

    @try_except_wrapper
    def add_config(self, *args):
        conf = Config()
        self.mod_manager.update_config_fields(conf)
        self.model.add_config(conf)

    @try_except_wrapper
    def remove_config(self, *args):
        self.model.remove_config()
        self.save_configs()

    @try_except_wrapper
    def select_config(self, config):
        self.model.current_config = config
        self.sender = None

    def update_config_field(self, field, value):
        if self.model.current_config:
            set_field_value(self.model.current_config, field, value)
            # self.logger.debug(f'{field} = {value}')

    def select_module(self, module_name):
        self.model.current_module = module_name

    @try_except_wrapper
    def send_request(self, *args):
        self.save_configs()
        module = self.model.current_module
        conf = self.model.current_config
        mod_params = conf.utils[module]

        self.logger.debug(module)
        self.logger.debug(str(mod_params))

        if self.sender is None:
            self.sender = Sender(self.logger,
                                 conf.host,
                                 self.model.login_pass,
                                 self.model.urls)
            self.sender.question_method = self.question_method
            if not self.sender.auth():
                self.sender = None
                return
        request = self.mod_manager.create_request(module)
        response = self.sender.send_request(conf.instance, request)
        if response is None:
            self.sender = None

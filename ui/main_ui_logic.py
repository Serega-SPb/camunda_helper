import base64
import logging
import os

import yaml
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QMenuBar, \
                            QMenu, QCheckBox, QListWidgetItem

from core import log_config
from core.decorators import try_except_wrapper
from core.config import Config
from core.sender import Request, Sender
from modules.manager import Manager as ModuleManager
from ui.additional_widgets import LoginDialog, ConfigWidget, InputMenuAction
from ui.main_ui import Ui_MainWindow

UI_DIR = os.path.dirname(__file__)
URLS_FILE = 'urls.yaml'
CONFIGS_FILE = 'configs.yaml'


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


class UiLogHandler(logging.Handler):
    def __init__(self, log_widget):
        super().__init__()
        self.widget = log_widget
        self.widget.setReadOnly(True)
        self.setFormatter(log_config.formatter)
        self.setLevel(log_config.STREAM_LOG_LVL)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class MainWindow(QMainWindow):
    TASK_FIELDS = {}

    def __init__(self, parent=None):
        self.configs = []
        self.urls = {'auth': '', 'engine': ''}
        super().__init__(parent)
        # uic.loadUi(os.path.join(UI_DIR, 'main.ui'), self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.mod_manager = ModuleManager()
        self.current_config = None
        self.logger = logging.getLogger(log_config.LOGGER_NAME)
        self.logger.addHandler(UiLogHandler(self.ui.logPtx))
        self.load_login()
        self.init_task_fields()
        self.init_ui()
        pass

    # region Properties

    @property
    def current_config(self):
        return self.__current_config

    @current_config.setter
    def current_config(self, value):
        self.__current_config = value
        if value:
            self.__select_config(value)
            self.ui.configParamsContainer.setEnabled(True)
        else:
            self.ui.configParamsContainer.setEnabled(False)

    @property
    def config_name(self):
        return self.ui.configNameTbx.text()

    @config_name.setter
    def config_name(self, value):
        self.ui.configNameTbx.setText(value)

    @property
    def host(self):
        return self.ui.hostTxb.text()

    @host.setter
    def host(self, value):
        self.ui.hostTxb.setText(value)

    @property
    def instance(self):
        return self.ui.instanceTxb.text()

    @instance.setter
    def instance(self, value):
        self.ui.instanceTxb.setText(value)

    @property
    def login_pass(self):
        return self.login

    @ login_pass.setter
    def login_pass(self, value):
        self.login = value
        if value:
            lg = self.login.split(':')[0]
        else:
            lg = 'anon'
        self.ui.loginLbl.setText(lg)

    # endregion

    def init_ui(self):
        self.load_urls()
        self.fill_menu_bar()
        self.load_configs()
        self.ui.addConfigBtn.clicked.connect(self.add_config)
        self.ui.removeConfigBtn.clicked.connect(self.remove_config)
        # self.ui.saveBtn.clicked.connect(self.save_configs)
        self.ui.sendRequestBtn.clicked.connect(self.send_request)
        self.ui.configList.itemSelectionChanged.connect(self.configs_selection_changed)
        self.ui.loginBtn.clicked.connect(self.open_login_win)

        self.ui_subscribe(self.ui.configNameTbx, 'name')
        self.ui_subscribe(self.ui.hostTxb, 'host')
        self.ui_subscribe(self.ui.instanceTxb, 'instance')

    def fill_menu_bar(self):

        def set_url(key, value):
            self.urls[key] = value

        self.ui.menuBar.clear()
        self.ui.urlMenus = []
        urls_menu = QMenu(self.ui.menuBar)
        urls_menu.setTitle('Urls')

        for n, u in self.urls.items():
            url_menu = InputMenuAction(self.ui.menuBar)
            url_menu.setObjectName(n)
            self.ui.urlMenus.append(url_menu)
            url_menu.label = n
            url_menu.valueLE.setText(u)
            url_menu.valueChanged.connect(set_url)
            urls_menu.addAction(url_menu.get_widget_action(urls_menu))

        self.ui.menuBar.addAction(urls_menu.menuAction())

    def init_task_fields(self):
        move_task = {
            'is_close': self.ui.closeTaskChbx,
            'is_start': self.ui.startTaskChbx,
            'close': self.ui.closeTaskTxb,
            'start': self.ui.startTaskTxb,
        }

        self.TASK_FIELDS['move_task'] = move_task

        for task, fields in self.TASK_FIELDS.items():
            for f, w in fields.items():
                self.ui_subscribe(w, f'utils.[{task}].[{f}]')

    def load_login(self):
        if not os.path.isfile('login.txt'):
            return
        with open('login.txt', 'rb') as file:
            data = file.read()
        self.login_pass = base64.b64decode(data).decode()

    def open_login_win(self):
        win = LoginDialog(self)
        win.show()
        win.exec_()
        if win.confirm:
            self.load_login()
            self.logger.info('Login updated')

    # region Event handlers

    def closeEvent(self, *args, **kwargs):
        self.save_urls()
        self.save_configs()

    def ui_subscribe(self, widget, config_field):
        def handler(value):
            if not self.current_config:
                return
            set_field_value(self.current_config, config_field, value)

        if isinstance(widget, QLineEdit):
            widget.textChanged.connect(handler)
            pass
        elif isinstance(widget, QCheckBox):
            widget.toggled.connect(handler)
            pass
        # elif isinstance(widget, QCheckBox):
        pass

    def configs_selection_changed(self):
        selected = self.ui.configList.selectedItems()
        self.current_config = selected[0].config if len(selected) > 0 else None

    # endregion

    def __add_config_widget(self, config):
        item = QListWidgetItem()
        item.config = config
        widget = ConfigWidget(config, self.ui.configList)

        item.setSizeHint(widget.sizeHint())
        self.ui.configList.addItem(item)
        self.ui.configList.setItemWidget(item, widget)

    @try_except_wrapper
    def load_urls(self):
        if not os.path.isfile(URLS_FILE):
            return
        with open(URLS_FILE, 'r', encoding='utf-8') as file:
            data = yaml.load(file, yaml.FullLoader)
        self.urls = {n: data.get(n, '') for n, u in self.urls.items()}
        self.logger.debug('urls loaded')

    @try_except_wrapper
    def save_urls(self):
        with open(URLS_FILE, 'w', encoding='utf-8') as file:
            yaml.dump(self.urls, file, default_flow_style=False)
        self.logger.debug('urls saved')

    @try_except_wrapper
    def load_configs(self):
        def check_utils(config):
            for t, field in self.TASK_FIELDS.items():
                if t not in config.utils:
                    config.utils[t] = {f: None for f in field.keys()}

        if not os.path.isfile(CONFIGS_FILE):
            return
        with open(CONFIGS_FILE, 'r', encoding='utf-8') as file:
            data = yaml.load(file, yaml.FullLoader)
        if not data:
            self.logger.warning(f'{CONFIGS_FILE} is empty')
            return
        self.configs = [Config.from_dict(d) for d in data]
        for c in self.configs:
            check_utils(c)
            self.__add_config_widget(c)
        self.logger.debug('configs loaded')

    @try_except_wrapper
    def save_configs(self, *args):
        data = [c.get_dict() for c in self.configs]
        with open(CONFIGS_FILE, 'w', encoding='utf-8') as file:
            yaml.dump(data, file, default_flow_style=False)
        self.logger.debug('configs saved')

    @try_except_wrapper
    def add_config(self, *args):
        conf = Config()
        for t, field in self.TASK_FIELDS.items():
            conf.utils[t] = {f: None for f in field.keys()}
        self.configs.append(conf)
        self.__add_config_widget(conf)

    @try_except_wrapper
    def remove_config(self, *args):
        items = [self.ui.configList.item(i) for i in range(self.ui.configList.count())]
        item = [i for i in items if hasattr(i, 'config') and i.config == self.current_config]
        if len(item) > 0:
            self.configs.remove(self.current_config)
            self.ui.configList.takeItem(self.ui.configList.row(item[0]))
            self.save_configs()

    def __select_config(self, config):
        self.config_name = config.name
        self.host = config.host
        self.instance = config.instance

        for t, field in self.TASK_FIELDS.items():
            for f, w in field.items():
                value = config.utils[t][f]
                if isinstance(w, QLineEdit):
                    w.setText(value if value else '')
                elif isinstance(w, QCheckBox):
                    w.setChecked(value if value else False)

    @try_except_wrapper
    def send_request(self, *args):
        curr_tab = self.ui.taskTabs.currentWidget()
        self.save_configs()

        conf = self.current_config
        request = Request.from_config(curr_tab.objectName(), conf)
        sender = Sender(conf.host, self.login_pass, self.logger)
        # self.logger.debug(self.login_pass)
        try:
            self.logger.info(sender.auth(request.urls['auth']))
        except Exception as e:
            self.logger.error(e)

        self.logger.debug(request.get_path(conf.host))
        self.logger.debug(request.body)

        resp = sender.send(request)
        self.logger.info(f'Response: {resp}')

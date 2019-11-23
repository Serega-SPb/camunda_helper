import logging

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QMenu, QTabWidget, \
                            QListWidgetItem, QLineEdit, QCheckBox

from core import log_config
from core.config import Config
from core.decorators import try_except_wrapper
from modules.manager import Manager as ModuleManager
from ui.main_ui import Ui_MainWindow
from ui.additional_widgets import InputMenuAction, ConfigWidget, LoginDialog


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


class MainView(QMainWindow):
    def __init__(self, model, controller, parent=None):
        super().__init__(parent)
        self.model = model
        self.controller = controller
        self.mod_manager = ModuleManager()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.logger = logging.getLogger(log_config.LOGGER_NAME)
        self.logger.addHandler(UiLogHandler(self.ui.logPtx))

        self.connect_widgets()
        self.connect_model_signals()
        self.controller_loads()
        self.load_modules()

    def controller_loads(self):
        self.controller.load_login()
        self.controller.load_urls()
        self.controller.load_configs()

    def connect_widgets(self):
        self.ui.loginBtn.clicked.connect(self.open_login_win)
        self.ui.addConfigBtn.clicked.connect(self.controller.add_config)
        self.ui.removeConfigBtn.clicked.connect(self.controller.remove_config)
        self.ui.sendRequestBtn.clicked.connect(self.controller.send_request)
        self.ui.configList.itemSelectionChanged.connect(self.configs_selection_changed)
        self.ui.taskTabs.currentChanged.connect(self.current_module_changed)

        self.config_field_changing(self.ui.configNameTbx, 'name')
        self.config_field_changing(self.ui.hostTxb, 'host')
        self.config_field_changing(self.ui.instanceTxb, 'instance')

    def connect_model_signals(self):
        self.model.login_changed.connect(self.ui.loginLbl.setText)
        self.model.urls_changed.connect(self.fill_menu_bar)
        self.model.configs_changed.connect(self.on_configs_changed)
        self.model.current_config_changed.connect(self.on_current_config_changed)
        self.model.config_added.connect(self.add_config_widget)
        self.model.config_added.connect(self.remove_config_widget)

    # region UI properties

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

    # endregion

    @try_except_wrapper
    def load_modules(self):
        modules = self.mod_manager.get_views()
        self.ui.taskTabs.clear()
        for name, wid in modules.items():
            wid.model.can_send_changed.connect(self.update_send_btn_status)
            wid.setObjectName(name)
            self.ui.taskTabs.addTab(wid, name.capitalize().replace('_', ' '))
            self.register_module_vars(name)

    @try_except_wrapper
    def register_module_vars(self, module_name):
        def connecting(s, f):
            s.connect(lambda v: self.controller.update_config_field(f, v))

        mod = self.mod_manager.get_model_by_name(module_name)
        for field in mod.__dict__.keys():
            prop = field[1:]
            signal = getattr(mod, f'{prop}_changed')
            field_path = f'utils.[{module_name}].[{prop}]'
            connecting(signal, field_path)

    def config_field_changing(self, widget, field):
        if isinstance(widget, QLineEdit):
            widget.textChanged.connect(
                lambda v: self.controller.update_config_field(field, v))
        elif isinstance(widget, QCheckBox):
            widget.toggled.connect(
                lambda v: self.controller.update_config_field(field, v))

    def on_configs_changed(self, configs):
        self.ui.configList.clear()
        for c in configs:
            self.add_config_widget(c)

    @try_except_wrapper
    @pyqtSlot(Config)
    def add_config_widget(self, config):
        item = QListWidgetItem()
        item.config = config
        widget = ConfigWidget(config, self.ui.configList)

        item.setSizeHint(widget.sizeHint())
        self.ui.configList.addItem(item)
        self.ui.configList.setItemWidget(item, widget)

    @try_except_wrapper
    @pyqtSlot(Config)
    def remove_config_widget(self, config):
        items = [self.ui.configList.item(i) for i in range(self.ui.configList.count())]
        item = [i for i in items if hasattr(i, 'config') and i.config == config]
        if len(item) > 0:
            self.ui.configList.takeItem(self.ui.configList.row(item[0]))

    @pyqtSlot(object)
    def on_current_config_changed(self, value):
        if value:
            self.__select_config(value)
            self.ui.configParamsContainer.setEnabled(True)
        else:
            self.ui.configParamsContainer.setEnabled(False)

    @try_except_wrapper
    def __select_config(self, config):
        self.config_name = config.name
        self.host = config.host
        self.instance = config.instance
        for name, fields in config.utils.items():
            model = self.mod_manager.get_model_by_name(name)
            for field, value in fields.items():
                setattr(model, field, value)

    @try_except_wrapper
    @pyqtSlot(dict)
    def fill_menu_bar(self, menus):
        self.ui.menuBar.clear()
        urls_menu = QMenu(self.ui.menuBar)
        urls_menu.setTitle('Urls')

        for n, u in menus.items():
            url_menu = InputMenuAction(self.ui.menuBar)
            url_menu.label = n
            url_menu.valueLE.setText(u)
            url_menu.valueChanged.connect(self.controller.update_url)
            urls_menu.addAction(url_menu.get_widget_action(urls_menu))

        self.ui.menuBar.addAction(urls_menu.menuAction())

    def open_login_win(self):
        win = LoginDialog(self)
        win.show()
        win.exec_()
        if win.confirm:
            self.controller.load_login()
            self.logger.info('Login updated')

    @try_except_wrapper
    def update_send_btn_status(self):
        current_module = self.ui.taskTabs.currentWidget()
        model = current_module.model
        self.ui.sendRequestBtn.setEnabled(model.can_send)

    def current_module_changed(self, ind):
        if ind < 0:
            return
        self.controller.select_module(
            self.ui.taskTabs.widget(ind).objectName())

    def configs_selection_changed(self):
        selected = self.ui.configList.selectedItems()
        self.controller.select_config(selected[0].config if len(selected) > 0 else None)

    def closeEvent(self, *args, **kwargs):
        self.controller.save_urls()
        self.controller.save_configs()

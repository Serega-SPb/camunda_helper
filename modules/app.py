from PyQt5.QtWidgets import *
from ui.additional_widgets import InputMenuAction


def get_view():
    m_win = QMainWindow()
    menu = QMenuBar(m_win)
    s_menu = QMenu(menu)
    s_menu.setTitle('Test')

    i1 = InputMenuAction()
    i1.label = 'Test_1'
    i1.valueLE.textChanged.connect(lambda x: print(x))

    s_menu.addAction(i1.get_widget_action(s_menu))
    i1.label = 'LABEL'

    menu.addAction(s_menu.menuAction())
    m_win.setMenuBar(menu)

    return m_win


def main():
    app = QApplication([])
    view = get_view()
    view.show()
    app.exec_()


if __name__ == '__main__':
    main()

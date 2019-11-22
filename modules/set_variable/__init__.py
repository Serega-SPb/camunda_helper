from .model import SVModel as Model
from .view import SVView as View
from .controller import SVController as Controller


def get_mvc():
    m = Model()
    c = Controller(m)
    v = View(m, c)
    return m, v, c

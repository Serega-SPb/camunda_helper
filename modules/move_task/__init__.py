from .model import MTModel as Model
from .view import MTView as View
from .controller import MTController as Controller


def get_mvc():
    m = Model()
    c = Controller(m)
    v = View(m, c)
    return m, v, c

from .model import SVModel as Model
from .view import SVView as View
from .controller import SVController as Controller
from .request import SVRequest as Request


def get_mvc():
    m = Model()
    c = Controller(m)
    v = View(m, c)
    return m, v, c


def get_request_cl(*args):
    return Request(*args)

from core.descriptors import NotifyProperty

NAME = '_name'
HOST = '_host'
INSTANCE = '_instance'
UTILS = 'utils'

U_MOVE = 'move'


class Config:

    __slots__ = (NAME, HOST, INSTANCE, UTILS)

    def __init__(self):
        self._name = NotifyProperty(NAME)
        self._host = NotifyProperty(HOST)
        self._instance = NotifyProperty(INSTANCE)
        self.utils = {}
        self.set_default()

    def set_default(self):
        self.name = ''
        self.host = ''
        self.instance = ''

    # region Properties
    @property
    def name(self):
        return self._name.get()

    @name.setter
    def name(self, value):
        self._name.set(value)

    @property
    def host(self):
        return self._host.get()

    @host.setter
    def host(self, value):
        self._host.set(value)

    @property
    def instance(self):
        return self._instance.get()

    @instance.setter
    def instance(self, value):
        self._instance.set(value)
    # endregion

    @classmethod
    def from_dict(cls, source):
        ins = cls()
        for s in cls.__slots__:
            f = getattr(ins, s)
            if isinstance(f, NotifyProperty):
                f.set(source[s])
            else:
                setattr(ins, s, source[s])
                # f = source[s]
        return ins

    """
        # self.configs = [
        #     Config.from_dict({'_name': 'test1', '_host': '127.0.0.1', '_instance': 'instance_1', 'utils': []}),
        #     Config.from_dict({'_name': 'test2', '_host': '127.0.0.2', '_instance': 'instance_2', 'utils': []}),
        #     Config.from_dict({'_name': 'test3', '_host': '127.0.0.3', '_instance': 'instance_3', 'utils': []}),
        # ]
    """

    def subscribe(self, name, func):
        f = getattr(self, f'_{name}')
        f += func

    def unsubscribe(self, name, func):
        f = getattr(self, f'_{name}')
        f -= func

    def get_dict(self):
        res = {}
        for s in self.__slots__:
            val = getattr(self, s, None)
            if isinstance(val, NotifyProperty):
                val = str(val)
            res[s] = val
        return res
        # return {s: getattr(self, s, None) for s in self.__slots__}

    def __str__(self):
        return f'{self.name} ({self.host})' if self.name else 'New config'

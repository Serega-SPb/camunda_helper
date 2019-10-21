class NotifyProperty:
    __slots__ = ('name', 'value', 'subscribers')

    def __init__(self, name):
        self.name = name
        self.subscribers = []
        self.value = None

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        [s(value) for s in self.subscribers if callable(s)]

    def __iadd__(self, other):
        self.subscribers.append(other)
        return self

    def __eq__(self, other):
        return self.value == other

    def __str__(self):
        return str(self.value)

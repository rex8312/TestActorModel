
from Singleton import *


class Event(list):
    __metaclass__ = Singleton

    def __init__(self):
        super(Event, self).__init__()
        self.event_manager = None
        self.name = None

    def add_handler(self, handler):
        self.append(handler)
        return self

    def remove_handler(self, handler):
        self.remove(handler)
        return self

    def fire(self, *args, **kwargs):
        for handler in self:
            handler(*args, **kwargs)

    __iadd__ = add_handler
    __isub__ = remove_handler
    __call__ = fire


class EventManager(dict):
    __metaclass__ = Singleton

    def __init__(self):
        super(EventManager, self).__init__()

    def __getattr__(self, event):
        return self[event]

    def __setattr__(self, event, value):
        self[event] = value

    def register_event(self, name):
        self[name] = Event()
        self[name].name = name
        self[name].event_manager = self
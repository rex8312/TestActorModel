from threading import Thread
from IActor import IActor
from Mailbox import Mailbox
from BasicMessage import *


class HandlerRegistry(dict):
    def __call__(self, typ):
        def register(func):
            self[typ] = func
            return func
        return register


class Actor(IActor):
    @classmethod
    def spawn(cls, *args, **kwargs):
        self = cls(*args, **kwargs)
        self.mailbox = Mailbox()
        self.start_thread(target=self.act, as_daemon=True)
        return self

    @classmethod
    def start_thread(cls, target, as_daemon, name=None):
        thread = Thread(target=target)
        if name:
            thread.setName(name)
        thread.setDaemon(as_daemon)
        thread.start()
        return thread

    def send(self, message, sender):
        if self.mailbox is None:
            raise ActorNotStartedError()
        else:
            self.mailbox.send(message, sender)

    def receive(self):
        if self.mailbox is None:
            raise ActorNotStartedError()
        else:
            return self.mailbox.receive()

    handles = HandlerRegistry()

    @classmethod
    def make_handles(*classes):
        return HandlerRegistry((typ, handler)
                               for cls in classes
                               for (typ, handler) in cls.handles.iteritems())

    def act(self):
        try:
            while True:
                message, sender = self.receive()
                registry = self.__class__.handles
                handler = registry.get(message.__class__) or registry.get(OtherMessage)
                if handler is not None:
                    handler(self, message, sender)
        except Stop:
            pass

    @handles(OtherMessage)
    def do_other(self, message, sender):
        pass

    @handles(Stop)
    def on_stop(self, message, sender):
        sender.send(Stopped(), self)
        raise message



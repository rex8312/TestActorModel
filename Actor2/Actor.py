import socket
import gevent
from gevent.queue import Queue
from Actor2.Singleton import *


class Actor(gevent.Greenlet):

    @classmethod
    def spawn(cls, *args, **kwargs):
        actor = cls(*args, **kwargs)
        actor.on_start()
        Registry().register(actor)
        actor.start(*args, **kwargs)
        return actor

    def __init__(self, *args, **kwargs):
        gevent.Greenlet.__init__(self)
        self.inbox = Queue()

    def on_start(self, *args, **kwargs):
        pass

    def tell(self, message, sender):
        self.inbox.put((message, sender))

    def on_receive(self, message, sender):
        raise NotImplemented()

    def _run(self):
        self.running = True

        while self.running:
            message, sender = self.inbox.get()
            self.on_receive(message, sender)

    def sleep(self, seconds):
        gevent.sleep(seconds)


class Registry(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(Registry, self).__init__()
        self.actors = list()

    def register(self, actor):
        self.actors.append(actor)

    def stop_all(self):
        gevent.joinall(self.actors)
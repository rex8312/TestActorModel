import socket
import gevent
from gevent.queue import Queue
from Actor2.Singleton import *


class Actor(gevent.Greenlet):

    @classmethod
    def spawn(cls, *args, **kwargs):
        actor = cls(*args, **kwargs)
        actor.on_start()
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


class ActorSystem(object):
    __metaclass__ = Singleton

    def __init__(self):
        super(ActorSystem, self).__init__()
        self.child_actors = list()

    def create(self, cls, *args, **kwargs):
        actor = cls.spawn(*args, **kwargs)
        actor.context = self
        self.child_actors.append(actor)
        return actor

    def stop_all(self):
        map(lambda x: x.tell("stop", None), self.child_actors)

    def join_all(self):
        gevent.joinall(self.child_actors)

    def sleep(self, seconds):
        gevent.sleep(seconds)
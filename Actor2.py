import gevent
from gevent.queue import Queue


class Actor(gevent.Greenlet):
    def __init__(self):
        self.inbox = Queue()
        gevent.Greenlet.__init__(self)

    def receive(self, message, sender):
        raise NotImplemented()

    def _run(self):
        self.running = True

        while self.running:
            message, sender = self.inbox.get()
            self.receive(message, sender)


if __name__ == '__main__':

    class Pinger(Actor):
        def receive(self, message, sender):
            print message
            ponger.inbox.put(('+', self))
            gevent.sleep(0)

    class Ponger(Actor):
        def receive(self, message, sender):
            print message
            pinger.inbox.put(('-', self))
            gevent.sleep(0)

    pinger = Pinger()
    ponger = Ponger()

    pinger.start()
    ponger.start()

    pinger.inbox.put(('start', None))

    gevent.joinall([pinger, ponger])
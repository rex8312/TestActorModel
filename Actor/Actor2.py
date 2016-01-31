import gevent
from gevent.queue import Queue, Empty
from BasicMessage import *


class Mailbox:
    def __init__(self):
        self.mailbox = Queue()

    def send(self, message, sender):
        self.mailbox.put((message, sender), block=False)

    def receive(self, timeout=None):
        return self.mailbox.get(block=True, timeout=timeout)


class Actor(gevent.Greenlet):
    @classmethod
    def spawn(cls, *args, **kwargs):
        self = cls(*args, **kwargs)
        self.mailbox = Mailbox()
        self.start()
        return self

    def send(self, message, sender):
        self.mailbox.send(message, sender)

    def _run(self):
        self.running = True

        while self.running:
            message, sender = self.mailbox.receive()
            self.receive(message, sender)

    def receive(self, message, sender):
        raise NotImplemented()


class Bridge(object):
    def __init__(self):
        self.mailbox = Mailbox()

    def send(self, message, sender):
            self.mailbox.send(message, sender)

    def call(self, target, request, timeout, default=None):
        self.send_request(target, request)
        return self.receive_response(timeout, default)

    def multi_call(self, targeted_requests, timeout, default=None):
        count = 0
        for target, request in targeted_requests:
            self.send_request(target, request)
            count += 1

        for _ in xrange(count):
            yield self.receive_response(timeout, default)

    def stop(self, actors, timeout):
        stop = Stop()
        # gevent.joinall([ping, pong])
        return list(self.multi_call(((actor, stop) for actor in actors), timeout, default=None))

    def send_request(self, target, request):
        target.send(request, self)

    def receive_response(self, timeout, default):
        try:
            message, sender = self.mailbox.receive(timeout=timeout)
            return message
        except Empty:
            return default


if __name__ == '__main__':

    class Ping(Actor):
        def receive(self, message, sender):
            print message
            if message is Stop:
                self.stop()
            else:
                pong.send('+', self)
            gevent.sleep(0)

    class Pong(Actor):
        def receive(self, message, sender):
            print message
            if message is Stop:
                self.stop()
            else:
                ping.send('-', self)
            gevent.sleep(0)

    ping = Ping.spawn()
    pong = Pong.spawn()
    bridge = Bridge()

    ping.send('start', None)
    bridge.stop([ping, pong], 1)
    gevent.joinall([ping, pong])

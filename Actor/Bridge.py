from IActor import IActor
from Mailbox import Mailbox
from gevent.queue import Empty
from BasicMessage import *


class Bridge(IActor):
    def __init__(self):
        IActor.__init__(self)
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
        return list(self.multi_call(((actor, stop) for actor in actors), timeout, default=None))

    def send_request(self, target, request):
        target.send(request, self)

    def receive_response(self, timeout, default):
        try:
            message, sender = self.mailbox.receive(timeout=timeout)
            return message
        except Empty:
            return default
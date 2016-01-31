
#from gevent.queue import Queue
from Queue import Queue


class Mailbox:
    def __init__(self):
        self.mailbox = Queue()

    def send(self, message, sender):
        self.mailbox.put((message, sender), block=False)

    def receive(self, timeout=None):
        return self.mailbox.get(block=True, timeout=timeout)

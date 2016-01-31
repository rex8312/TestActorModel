from threading import Thread, Event
from Queue import Queue, Empty


class IActor:
    pass


class HandlerRegistry(dict):
    def __call__(self, typ):
        def register(func):
            self[typ] = func
            return func
        return register


OtherMessage = "Other Message"


class Stop(Exception):
    def __repr__(self):
        return "Stop()"


class Stopped:
    def __repr__(self):
        return "Stopped()"


class ActorNotStartedError(Exception):
    def __init__(self):
        Exception.__init__(self, "actor not started")


class Actor(IActor):
    @classmethod
    def spawn(cls, *args, **kwargs):
        self = cls(*args, **kwargs)
        self.mailbox = Mailbox()
        start_thread(target=self.act, as_daemon=True)
        return self

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

    def act(self):
        self.handleMessages()

    handles = HandlerRegistry()

    @classmethod
    def makeHandles(*classes):
        return HandlerRegistry((typ, handler) for cls in classes for (typ, handler) in cls.handles.iteritems())

    def handleMessages(self):
        try:
            while True:
                message, sender = self.receive()
                self.handleMessageWithRegistry(message, sender)
        except Stop:
            pass

    def handleMessageWithRegistry(self, message, sender):
        registry = self.__class__.handles
        handler = registry.get(message.__class__) or registry.get(OtherMessage)
        if handler is not None:
            handler(self, message, sender)

    @handles(OtherMessage)
    def doOther(self, message, sender):
        pass

    @handles(Stop)
    def onStop(self, message, sender):
        sender.send(Stopped(), self)
        raise message


def start_thread(target, as_daemon, name = None):
    thread = Thread(target=target)
    if name:
        thread.setName(name)
    thread.setDaemon(as_daemon)
    thread.start()
    return thread


class Mailbox:
    def __init__(self):
        self.mailbox = Queue()

    def send(self, message, sender):
        self.mailbox.put((message, sender), block=False)

    def receive(self, timeout=None):
        return self.mailbox.get(block=True, timeout=timeout)


class Bridge(IActor):
    def __init__(self):
        self.mailbox = Mailbox()

    def send(self, message, sender):
        self.mailbox.send(message, sender)

    def call(self, target, request, timeout, default=None):
        self.sendRequest(target, request)
        return self.receiveResponse(timeout, default)

    def multiCall(self, targeted_requests, timeout, default=None):
        count = 0
        for target, request in targeted_requests:
            self.sendRequest(target, request)
            count += 1

        for _ in xrange(count):
            yield self.receiveResponse(timeout, default)

    def stop(self, actors, timeout):
        stop = Stop()
        return list(self.multiCall(((actor, stop) for actor in actors), timeout, default=None))

    def sendRequest(self, target, request):
        target.send(request, self)

    def receiveResponse(self, timeout, default):
        try:
            message, sender = self.mailbox.receive(timeout=timeout)
            return message
        except Empty:
            return default
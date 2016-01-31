
import time
from Actor.Bridge import Bridge
from Actor.Actor import Actor


if __name__ == '__main__':
    class Start:
        def __init__(self, target):
            self.target = target

    class Ping:
        def __repr__(self):
            return 'Ping()'

    class Pong:
        def __repr__(self):
            return 'Pong()'

    class Pinger(Actor):
        handles = Actor.make_handles()

        @handles(Start)
        def on_start(self, start, sender):
            start.target.send(Ping(), self)

        @handles(Pong)
        def on_pong(self, pong, sender):
            print "-",
            sender.send(Ping(), self)

    class Ponger(Actor):
        handles = Actor.make_handles()

        @handles(Ping)
        def on_ping(self, ping, sender):
            print "+",
            sender.send(Pong(), self)

    bridge = Bridge()
    pinger = Pinger.spawn()
    ponger = Ponger.spawn()
    pinger.send(Start(ponger), sender=None)
    time.sleep(0.1)
    bridge.stop([pinger, ponger], 1)
# -*- coding: utf-8 -*-

from Actor2.Actor import Actor
from Actor2.Actor import ActorSystem


class Pinger(Actor):
    def on_start(self):
        self.count = 0
        self.pong = ActorSystem().create(Ponger)

    def on_receive(self, message, sender):
        print(message, self.count)

        if sender is None:
            self.pong.tell('+', self)
        else:
            sender.tell('+', self)

        self.count += 1
        self.sleep(0)


class Ponger(Actor):
    def on_start(self):
        self.count = 0

    def on_receive(self, message, sender):
        print(message, self.count)

        sender.tell('-', self)

        self.count += 1
        self.sleep(0)


if __name__ == "__main__":
    ping = ActorSystem().create(Pinger)
    ping.tell('start', None)
    ActorSystem().sleep(1)


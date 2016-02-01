# -*- coding: utf-8 -*-

from Actor2.Actor import Actor
from Actor2.Actor import ActorSystem


class Pinger(Actor):
    def on_start(self):
        self.child = ActorSystem().create(Ponger)

    def on_receive(self, message, sender):
        self.sleep(0)
        future = self.child.ask(message)

        future.on_ready(self._print)

    @staticmethod
    def _print(v):
        print v


class Ponger(Actor):
    def on_receive(self, message, sender):
        self.sleep(1)
        return message + 1


if __name__ == "__main__":
    ping = ActorSystem().create(Pinger)
    ping.tell(1, None)
    print 'start'
    ActorSystem().sleep(5)

    # TODO: become, unbecome 구현

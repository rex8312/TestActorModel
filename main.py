
from Actor1 import Actor, OtherMessage, Bridge


if __name__ == "__main__":

    import time

    class GetInventory:
        pass

    class Task:
        def __init__(self, input, destination):
            self.input = input
            self.destination = destination

    class Worker(Actor):
        handles = Actor.makeHandles()

        def __init__(self, skill):
            self.skill = skill

        @handles(Task)
        def onTask(self, task, sender):
            output = self.skill(task.input)
            task.destination.send(output, self)

    class Warehouse(Actor):
        handles = Actor.makeHandles()

        def __init__(self):
            self.inventory = list()

        @handles(GetInventory)
        def onGetInventory(self, message, sender):
            sender.send(list(self.inventory), self)

        @handles(OtherMessage)
        def onTaskResult(self, result, sender):
            self.inventory.append(result)

    worker = Worker.spawn(lambda x: x * 2)
    positives = Warehouse.spawn()
    negatives = Warehouse.spawn()
    bridge = Bridge()

    for var in [1, 2, 3, -2, -4, -6]:
        warehouse = positives if var >= 0 else negatives
        worker.send(Task(var, warehouse), sender=None)

    print bridge.call(positives, GetInventory(), 1.0)
    print bridge.call(negatives, GetInventory(), 1.0)
    print bridge.stop([worker, positives, negatives], 1.0)

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
        handles = Actor.makeHandles()

        @handles(Start)
        def onStart(self, start, sender):
            start.target.send(Ping(), self)

        @handles(Pong)
        def onPong(self, pong, sender):
            print "-",
            sender.send(Ping(), self)

    class Ponger(Actor):
        handles = Actor.makeHandles()

        @handles(Ping)
        def onPing(self, ping, sender):
            print "+",
            sender.send(Pong(), self)

    pinger = Pinger.spawn()
    ponger = Ponger.spawn()
    pinger.send(Start(ponger), sender=None)
    time.sleep(0.1)
    bridge.stop([pinger, ponger], 1)


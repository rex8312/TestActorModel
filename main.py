
from Actor.Actor import Actor
from Actor.Bridge import Bridge
from Actor.BasicMessage import *


if __name__ == "__main__":

    class GetInventory:
        def __init__(self):
            pass

    class Task:
        def __init__(self, inputs, destination):
            self.input = inputs
            self.destination = destination

    class Worker(Actor):
        handles = Actor.make_handles()

        def __init__(self, skill):
            Actor.__init__(self)
            self.skill = skill

        @handles(Task)
        def on_task(self, task, sender):
            output = self.skill(task.input)
            task.destination.send(output, self)

    class Warehouse(Actor):
        handles = Actor.make_handles()

        def __init__(self):
            Actor.__init__(self)
            self.inventory = list()

        @handles(GetInventory)
        def on_get_inventory(self, message, sender):
            sender.send(list(self.inventory), self)

        @handles(OtherMessage)
        def on_task_result(self, result, sender):
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




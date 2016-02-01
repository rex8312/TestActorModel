
from threading import Timer


class Scheduler:
    @staticmethod
    def ticking(interval, func, iteration=0):
        if iteration != 1:
            Timer(interval, Scheduler.ticking, [interval, func, 0 if iteration == 0 else iteration - 1]).start()
        func()



OtherMessage = "Other Message"


class Stop(Exception):
    def __repr__(self):
        return "Stop()"


class Stopped:
    def __init__(self):
        pass

    def __repr__(self):
        return "Stopped()"


class ActorNotStartedError(Exception):
    def __init__(self):
        Exception.__init__(self, "actor not started")
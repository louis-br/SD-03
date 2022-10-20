from Utils.Event import Event


def subscribe(event):
    def decorator(method):
        method.__event__ = event
        return method
    return decorator


def subscribed_class(old_class):
    old_class.__eventDict__ = {}
    for attr in dir(old_class):
        attr = getattr(old_class, attr, None)
        event = getattr(attr, "__event__", None) if attr else None
        if event:
            old_class.__eventDict__[event] = attr
    return old_class


class State:
    def __init__(self):
        self.context = None

    def execute(self, event: Event):
        eventClass = event.__class__
        if eventClass not in self.__eventDict__:
            return
        method = self.__eventDict__[eventClass]
        method(self, event)

    def set_context(self, context):
        self.context = context

    def change_state(self, state):
        if not self.context:
            return
        self.context.change_state(state)

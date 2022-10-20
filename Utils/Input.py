from Utils.Event import Event
from Utils.EventHistory import EventHistory


class KeyboardEvent(Event):
    pass


class Input():
    def __init__(self, context: EventHistory):
        self.context = context

    def start(self):
        try:
            while True:
                value = input()
                self.context.add_and_process(KeyboardEvent(value))
        except KeyboardInterrupt:
            pass

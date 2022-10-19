from Utils.Event import Event
from Utils.State import State

class MenuState(State):
    def __init__(self):
        pass

    def execute(self, event: Event):
        super().execute(event)
        self.render()

    def render(self):
        pass
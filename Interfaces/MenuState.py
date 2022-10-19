from Interfaces.Event import Event
from Interfaces.State import State

class MenuState(State):
    def __init__(self):
        pass

    def execute(self, event: Event):
        super().execute(event)
        self.render()

    def render(self):
        pass
from Utils.MenuState import MenuState
from Utils.Input import KeyboardEvent
from Utils.State import State, subscribe, subscribed_class


@subscribed_class
class AlertEventMenu(MenuState):
    def __init__(self, lastState: State, appointment: dict[str]):
        super().__init__()
        self.lastState: State = lastState
        self.appointment: dict[str] = appointment

    def render(self):
        self.clear()
        print("Appointment alert: ")
        print(self.appointment)

    @subscribe(KeyboardEvent)
    def keyboard_input(self, event: KeyboardEvent):
        self.change_state(self.lastState)

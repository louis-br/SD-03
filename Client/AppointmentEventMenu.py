from Client.DateMenu import DateMenu, DateSetEvent
from Utils.Input import KeyboardEvent
from Utils.MenuState import MenuState
from Utils.State import State, subscribe, subscribed_class
from datetime import datetime


@subscribed_class
class AppointmentEventMenu(MenuState):
    def __init__(self, client, lastState: State, appointment: dict[str]):
        super().__init__()
        self.client = client
        self.lastState: State = lastState
        self.appointment: dict[str] = appointment
        self.alert: datetime = None

    def render(self):
        self.clear()
        print("You have been invited to a new event: ")
        print(self.appointment)
        print("Would you like to participate?")
        self.options = [
            "Ignore event",
            f'Create alert (Alert: {self.alert})',
            "Participate",
        ]
        self.print_options()
        print("Option: ", end="")

    def participate(self):
        self.client.register_alert(self.appointment['name'], self.alert)

    @subscribe(DateSetEvent)
    def date_set(self, event: DateSetEvent):
        self.alert = event.value

    @subscribe(KeyboardEvent)
    def keyboard_input(self, event: KeyboardEvent):
        self.set_option(event)
        if event.value == "":
            print(self.selectedOption)
            input()
            if self.selectedOption == 1:
                self.change_state(DateMenu(self))
            elif self.selectedOption == 2:
                self.participate()
                self.change_state(self.lastState)
            else:
                self.change_state(self.lastState)


import Client.Client

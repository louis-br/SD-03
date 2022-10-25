from Utils.Event import Event
from Client.MenuData import MenuData
from Client.PromptMenu import PromptMenu, PromptAnsweredEvent
from Client.DateMenu import DateMenu, DateSetEvent
from Utils.Input import KeyboardEvent
from Utils.MenuState import MenuState, RenderEvent
from Utils.State import State, subscribe, subscribed_class
from datetime import datetime


class NewAppointmentEvent(Event):
    appointment: str = ""
    users: list[str] = []
    alert: datetime = None


@subscribed_class
class NewAppointmentMenu(MenuState):
    def __init__(self, lastState: State, data: MenuData = MenuData()):
        super().__init__()
        self.data: MenuData = data
        self.lastState: State = lastState
        self.optionsValues = [
            lambda: self.change_state(PromptMenu(lastState=self, key="appointment", string="name")),
            lambda: self.change_state(DateMenu(self, key="date")),
            lambda: self.change_state(DateMenu(self, key="alert")),
            lambda: self.change_state(PromptMenu(lastState=self, key="users", string="users")),
            lambda: self.validate()
        ]
        self.event: NewAppointmentEvent = NewAppointmentEvent(datetime.now())

    def render(self):
        self.clear()
        print(f'User: {self.data.user}')
        print("Edit appointment")
        self.options = [
            f'Name: {self.event.appointment}',
            f'Date: {self.event.value}',
            f'Alert: {self.event.alert}',
            f'Invited users: {self.event.users}',
            "Submit"
        ]
        self.print_options()
        print("Option: ", end="")

    def validate(self):
        self.change_state(self.lastState)
        self.context.add_and_process(self.event)

    @subscribe(DateSetEvent)
    def date_set(self, event: DateSetEvent):
        if event.key == "date":
            self.event.value = event.value
        else:
            self.event.alert = event.value

    @subscribe(PromptAnsweredEvent)
    def prompt_answer(self, event: PromptAnsweredEvent):
        key, value = event.key, event.value
        if key == "users":
            value = value.split(",")
            self.event.users = value
        else:
            self.event.appointment = value

    @subscribe(KeyboardEvent)
    def keyboard_input(self, event: KeyboardEvent):
        self.set_option(event)
        if event.value == "":
            self.optionsValues[self.selectedOption]()

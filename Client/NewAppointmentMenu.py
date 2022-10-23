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


@subscribed_class
class NewAppointmentMenu(MenuState):
    def __init__(self, lastState: State, data: MenuData = MenuData()):
        super().__init__()
        self.data = data
        self.lastState = lastState
        self.optionsValues = [
            lambda: self.change_state(
                PromptMenu(lastState=self, key="appointment", string="name")
            ),
            lambda: self.change_state(DateMenu(self)),
            lambda: self.change_state(
                PromptMenu(lastState=self, key="users", string="users")
            ),
            lambda: self.validate()
        ]
        self.event = NewAppointmentEvent(datetime.now())

    def render(self):
        self.clear()
        print(f'User: {self.data.userStatus["user"]}')
        print("Edit appointment")
        self.options = [
            f'Name: {self.event.appointment}',
            f'Date: {self.event.value}',
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
        self.event.value = event.value

    @subscribe(PromptAnsweredEvent)
    def prompt_answer(self, event: PromptAnsweredEvent):
        key, value = event.key, event.value
        if key == "users":
            value = value.split(",")
            self.event.users = value
        else:
            self.event.appointment = value

    @subscribe(KeyboardEvent)
    def char_typed(self, event: KeyboardEvent):
        self.set_option(event)
        if event.value == "":
            self.optionsValues[self.selectedOption]()

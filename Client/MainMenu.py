from Client.Client import Client
from Client.MenuData import MenuData
from Client.PromptMenu import PromptMenu, PromptAnsweredEvent
from Client.NewAppointmentMenu import NewAppointmentMenu, NewAppointmentEvent
from Utils.Input import KeyboardEvent
from Utils.MenuState import MenuState
from Utils.State import subscribe, subscribed_class


@subscribed_class
class MainMenu(MenuState):
    def __init__(self, data: MenuData = MenuData()):
        super().__init__()
        self.data: MenuData = data
        self.status: str = ""
        self.options: list[str] = [
            "Register user",
            "Register appointment",
            "Cancel appointment",
            "Cancel alert",
            "Show appointments"
        ]
        self.optionsValues = [
            (lambda: self.change_state(PromptMenu(lastState=self, key=0, string="user")), lambda e: self.register_user(e)),
            (lambda: self.change_state(NewAppointmentMenu(self, self.data)), lambda e: self.register_appointment(e)),
            (lambda: self.change_state(PromptMenu(lastState=self, key=2, string="appointment")), lambda e: self.cancel_appointment(e)),
            (lambda: self.change_state(PromptMenu(lastState=self, key=3, string="appointment")), lambda e: self.cancel_alert(e)),
            (lambda: self.show_appointments(), lambda: None)
        ]

    def set_client(self, client: Client):
        self.client = client

    def render(self):
        self.clear()
        print(f'User: {self.data.user}')
        print(f'Status: {self.status}')
        self.print_options()
        print("Option: ", end="")

    def validate(self):
        option = self.selectedOption
        if option < len(self.optionsValues):
            self.optionsValues[option][0]()

    def register_user(self, event: PromptAnsweredEvent):
        user = event.value
        self.data.user = user
        self.client.register_user(user)
        self.status = f'Registered user: {event.value}'

    def register_appointment(self, event: NewAppointmentEvent):
        name = event.appointment
        date = event.value
        guests = {guest: True for guest in event.users}
        alerts = {}
        self.client.register_appointment(name, date, guests, alerts)
        self.status = f'Registered appointment: {name} {date}'

    def cancel_appointment(self, event: PromptAnsweredEvent):
        self.client.cancel_appointment(event.value)
        self.status = f'Canceled appointment: {event.value}'

    def cancel_alert(self, event: PromptAnsweredEvent):
        self.client.cancel_alert(event.value)
        self.status = f'Canceled alert: {event.value}'

    def show_appointments(self):
        appointments = self.client.get_appointments()
        if appointments:
            for appointment in appointments:
                print(appointment)
        else:
            print("No appointments found. ")
        input()

    @subscribe(PromptAnsweredEvent)
    def prompt_answer(self, event: PromptAnsweredEvent):
        self.optionsValues[event.key][1](event)

    @subscribe(NewAppointmentEvent)
    def new_appointment(self, event: NewAppointmentEvent):
        self.register_appointment(event)

    @subscribe(KeyboardEvent)
    def keyboard_input(self, event: KeyboardEvent):
        self.set_option(event)
        if event.value == "":
            self.validate()

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
        self.data = data
        self.options = [
            "Register user",
            "Register appointment",
            "Cancel appointment",
            "Cancel alert",
            "Show appointments"
        ]
        self.optionsValues = [
            (lambda: self.change_state(
                PromptMenu(lastState=self, key=0, string="user")
            ),
                lambda e: self.register_user(e)
            ),
            (lambda: self.change_state(
                NewAppointmentMenu(self, self.data)
            ),
                lambda e: self.register_appointment(e)
            ),
            (lambda: self.change_state(
                PromptMenu(lastState=self, key=2, string="appointment")
            ),
                lambda e: self.cancel_appointment(e)
            ),
            (lambda: self.change_state(
                PromptMenu(lastState=self, key=3, string="appointment")
            ),
                lambda e: self.cancel_alert(e)
            ),
            (lambda: None, lambda: None)
        ]

    def set_client(self, client: Client):
        self.client = client

    def render(self):
        self.clear()
        print(f'User: {self.data.userStatus["user"]}\
 ({self.data.userStatus["status"]})')
        self.print_options()
        print("Option: ", end="")

    def validate(self):
        option = self.selectedOption
        if option < len(self.optionsValues):
            print("Option: ", self.optionsValues[option])
            self.optionsValues[option][0]()

    def register_user(self, event: PromptAnsweredEvent):
        print("Registered user: ", event.value)
        self.data.userStatus['user'] = event.value
    #   self.data.userStatus['status'] = "Registering"
        input()

    def register_appointment(self, event: NewAppointmentEvent):
        print("Registered appointment: ", event.value)
        input()

    def cancel_appointment(self, event: PromptAnsweredEvent):
        print("Canceled appointment: ", event.value)
        input()

    def cancel_alert(self, event: PromptAnsweredEvent):
        print("Canceled alert: ", event.value)
        input()

    @subscribe(PromptAnsweredEvent)
    def prompt_answer(self, event: PromptAnsweredEvent):
        self.optionsValues[event.key][1](event)

    @subscribe(NewAppointmentEvent)
    def new_appointment(self, event: NewAppointmentEvent):
        self.register_appointment(event)

    @subscribe(KeyboardEvent)
    def char_typed(self, event: KeyboardEvent):
        self.set_option(event)
        if event.value == "":
            self.validate()

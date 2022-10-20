from Client.MenuData import MenuData
from Client.RegisterUserMenu import RegisterUserMenu
from Utils.Input import KeyboardEvent
from Utils.MenuState import MenuState, RenderEvent
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
        self.transitions = [
            RegisterUserMenu
        ]

    def render(self):
        self.clear()
        print("User:", self.data.user)
        self.print_options()
        print("Option: ", end="")

    def validate(self):
        option = self.selectedOption
        if option < len(self.transitions):
            state = self.transitions[option]
            self.change_state(state(self.data))

    @subscribe(KeyboardEvent)
    def char_typed(self, event: KeyboardEvent):
        self.set_option(event)
        if event.value == "":
            self.validate()

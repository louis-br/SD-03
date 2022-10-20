from Client.MenuData import MenuData
from Utils.Input import KeyboardEvent
from Utils.MenuState import MenuState, RenderEvent
from Utils.State import subscribe, subscribed_class

@subscribed_class
class RegisterUserMenu(MenuState):
    def __init__(self, data: MenuData=MenuData()):
        from Client.MainMenu import MainMenu
        super().__init__()
        self.data = data

    def render(self):
        self.clear()
        print("Enter user: ", end="")

    @subscribe(KeyboardEvent)
    def char_typed(self, event: KeyboardEvent):
        self.data.user = event.value
        self.change_state(Client.MainMenu.MainMenu(self.data))

import Client.MainMenu
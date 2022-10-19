from Utils.Event import Event
from Utils.MenuState import MenuState
from Utils.State import subscribe, subscribed_class

class MainMenuEvent(Event): base = None

class CharTypedEvent(MainMenuEvent): pass

@subscribed_class
class MainMenu(MenuState):
    def __init__(self):
        pass

    def render(self):
        pass

    @subscribe(CharTypedEvent)
    def char_typed(self, event: CharTypedEvent):
        print("Char typed: ", event, event.name, event.value)
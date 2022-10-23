from typing import Any
from Utils.Event import Event
from Client.MenuData import MenuData
from Utils.Input import KeyboardEvent
from Utils.MenuState import MenuState
from Utils.State import State, subscribe, subscribed_class


class PromptAnsweredEvent(Event):
    key: Any
    string: str


@subscribed_class
class PromptMenu(MenuState):
    def __init__(self, lastState: State, key: Any = "", string: str = "", data: MenuData = MenuData()):
        super().__init__()
        self.data = data
        self.lastState = lastState
        self.key = key
        self.string = string

    def render(self):
        self.clear()
        print(f'Enter {self.string}: ', end="")

    @subscribe(KeyboardEvent)
    def char_typed(self, event: KeyboardEvent):
        self.change_state(self.lastState)
        answer = PromptAnsweredEvent(event.value)
        answer.key = self.key
        answer.string = self.string
        self.context.add_and_process(answer)

from typing import Any
from Utils.Event import Event
from Utils.Input import KeyboardEvent
from Utils.MenuState import MenuState
from Utils.State import State, subscribe, subscribed_class


class PromptAnsweredEvent(Event):
    key: Any
    string: str


@subscribed_class
class PromptMenu(MenuState):
    def __init__(self, lastState: State, key: Any = "", string: str = ""):
        super().__init__()
        self.lastState: State = lastState
        self.key: Any = key
        self.string: str = string

    def render(self):
        self.clear()
        print(f'Enter {self.string}: ', end="")

    @subscribe(KeyboardEvent)
    def keyboard_input(self, event: KeyboardEvent):
        self.change_state(self.lastState)
        answer = PromptAnsweredEvent(event.value)
        answer.key = self.key
        answer.string = self.string
        self.context.add_and_process(answer)

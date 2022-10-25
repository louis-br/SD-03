from typing import Any
from Utils.Event import Event
from Utils.Input import KeyboardEvent
from Utils.MenuState import MenuState, RenderEvent
from Utils.State import State, subscribe, subscribed_class
from datetime import datetime


class DateSetEvent(Event):
    key: Any
    pass


def get_datetime_dict(d: datetime):
    return {
        'year': d.year,
        'month': d.month,
        'day': d.day,
        'hour': d.hour,
        'minute': d.minute,
        'second': d.second,
        'microsecond': 0
    }


@subscribed_class
class DateMenu(MenuState):
    def __init__(self, lastState: State, key: Any = ""):
        super().__init__()
        self.key: Any = key
        self.lastState: State = lastState
        self.attributes: list[str] = ["year", "month", "day", "hour", "minute", "second"]
        self.newDatetime: dict[str, int] = {}
        self.currentAttribute: str = ""
        self.calculate_datetime()

    def render(self):
        self.clear()
        print("Date: ")
        self.calculate_datetime()
        self.options = [
            "Reset",
            f'Year: {self.datetime.year}',
            f'Month: {self.datetime.month}',
            f'Day: {self.datetime.day}',
            f'Hour: {self.datetime.hour}',
            f'Minute: {self.datetime.minute}',
            f'Second: {self.datetime.second}',
            "Submit"
        ]
        self.print_options()
        if self.currentAttribute:
            print(f'{self.currentAttribute}: ', end="")
        else:
            print("Option: ", end="")

    def calculate_datetime(self):
        self.datetime: datetime = datetime.now()
        now = get_datetime_dict(self.datetime)
        for attr in self.attributes:
            if attr in self.newDatetime:
                now[attr] = self.newDatetime[attr]
        self.datetime: datetime = datetime(**now)

    def reset(self):
        self.newDatetime = {}

    def validate(self):
        self.change_state(self.lastState)
        event = DateSetEvent(self.datetime)
        event.key = self.key
        self.context.add_and_process(event)

    @subscribe(KeyboardEvent)
    def keyboard_input(self, event: KeyboardEvent):
        if self.currentAttribute != "" and event.value.isdigit():
            self.newDatetime[self.currentAttribute] = int(event.value)
            self.currentAttribute = ""
            return
        if event.value == "":
            option = self.selectedOption
            if option == 0:
                self.reset()
            elif option == len(self.options) - 1:
                self.validate()
            else:
                self.currentAttribute = self.attributes[option - 1]
            return
        self.set_option(event)

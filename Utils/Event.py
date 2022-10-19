from typing import Any

class Event:
    def __init__(self, value: Any=None, name: str=None):
        self.name = name if name else self.__class__.__name__
        self.value = value
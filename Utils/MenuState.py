from Utils.Event import Event
from Utils.State import State
from Utils.Input import KeyboardEvent


class RenderEvent(Event):
    pass


class MenuState(State):
    def __init__(self):
        super().__init__()
        self.options: list[str] = []
        self.selectedOption: int = 0

    def execute(self, event: Event):
        super().execute(event)
        self.render()

    def print_options(self):
        for option in range(len(self.options)):
            head = f' {option+1}.'
            if option == self.selectedOption:
                head = ">" + head[1:]
            print(head, self.options[option])

    def set_option(self, event: KeyboardEvent):
        for word in event.value.split(" "):
            if not word.isdigit():
                continue
            word = int(word) - 1
            if word >= 0 and word < len(self.options):
                self.selectedOption = word
                return True
        return False

    def set_context(self, context):
        super().set_context(context)
        context.add_and_process(RenderEvent())

    def clear(self):
        print("\x1B[1J")
        print("\n" * 20)

    def render(self):
        pass

from Interfaces.EventHistory import EventHistory
from MainMenu import MainMenu, CharTypedEvent

menu: MainMenu = MainMenu()
history: EventHistory = EventHistory(menu)

history.add_and_process(CharTypedEvent("a"))
from Utils.EventHistory import EventHistory
from Utils.Input import Input
from Client.MainMenu import MainMenu

menu = MainMenu()
history = EventHistory(menu)
keyboardInput = Input(history)

keyboardInput.start()

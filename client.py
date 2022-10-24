from Utils.EventHistory import EventHistory
from Utils.Input import Input
from Client.MainMenu import MainMenu
from Client.Client import Client

menu = MainMenu()
history = EventHistory(menu)
keyboardInput = Input(history)

client = Client("127.0.0.1", 9090, "Agenda")
menu.set_client(client)
client.register_user("user")

keyboardInput.start()
client.shutdown()

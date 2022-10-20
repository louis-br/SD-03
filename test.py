import Pyro5.api

nameserver = Pyro5.api.locate_ns("127.0.0.1", 9090)
uri = nameserver.lookup("Agenda")
print(uri)
server = Pyro5.api.Proxy(uri)
server.register_user()

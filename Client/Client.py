import Pyro5.api
from concurrent.futures import ThreadPoolExecutor
from Pyro5.server import expose


class Client():
    def __init__(self, nameserver: str, port: int, service: str):
        self.service = service
        self.nameserver = Pyro5.api.locate_ns(nameserver, port)
        self.serverURI = self.nameserver.lookup(service)
        self.server = Pyro5.api.Proxy(self.serverURI)

        self.daemon = Pyro5.server.Daemon()
        self.URI = self.daemon.register(self)
        self.thread = ThreadPoolExecutor()
        self.thread.submit(self.request_loop)

    def request_loop(self):
        self.daemon.requestLoop()

    def shutdown(self):
        self.server._pyroRelease()
        self.daemon.shutdown()
        self.thread.shutdown(True)

    def __del__(self):
        self.shutdown()

    def register_user(self, user: str):
        self.publickey = self.server.register_user(user, self.URI)
        print(self.publickey)

    @expose
    def alert_event(self):
        print("Alert!")

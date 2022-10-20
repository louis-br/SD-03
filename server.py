import Pyro5.nameserver
import Pyro5.server
from concurrent.futures import ThreadPoolExecutor

from Server.Server import Server

daemon = Pyro5.server.Daemon()
nameserverUri, nameserverDaemon, _ = Pyro5.nameserver.start_ns()

nameserver = nameserverDaemon.nameserver
uri = daemon.register(Server)
nameserver.register("Agenda", uri)

print("Starting nameserver: ", nameserverUri)


def run_nameserver():
    nameserverDaemon.requestLoop()


thread = ThreadPoolExecutor()
thread.submit(run_nameserver)

print("Server URI: ", uri)
print("Pyro daemon started: ")
daemon.requestLoop()

nameserverDaemon.shutdown()
thread.shutdown(True)

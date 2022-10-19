import queue
from queue import Queue
from threading import Semaphore
from Utils.Event import Event
from Utils.State import State

class EventHistory:
    def __init__(self, initialState: State):
        self.queue = Queue()
        self.mutex = Semaphore()
        self.change_state(initialState)

    def process(self, block=False):
        if not self.mutex.acquire(blocking=False): return
        try:
            while True:
                event = self.queue.get(block)
                self.state.execute(event)
        except queue.Empty:
            pass
        self.mutex.release()

    def add_and_process(self, event: Event, block=False):
        self.add(event)
        self.process(block)

    def change_state(self, state: State):
        self.state = state
        self.state.set_context(self)

    def add(self, event: Event):
        self.queue.put(event)
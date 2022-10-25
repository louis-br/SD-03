import queue
from queue import Queue
from threading import Lock
from Utils.Event import Event
from Utils.State import State


class EventHistory:
    def __init__(self, initialState: State):
        self.queue: Queue = Queue()
        self.mutex: Lock = Lock()
        self.stateMutex: Lock = Lock()
        self.change_state(initialState)

    def process(self, block=False):
        if not self.mutex.acquire(blocking=False):
            return
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
        with self.stateMutex:
            self.state: State = state
            self.state.set_context(self)

    def add(self, event: Event):
        self.queue.put(event)

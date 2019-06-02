import collections
import threading
from time import time


class BlockingCircularBuffer(collections.deque):

    def __init__(self, max_length: int = None):
        if max_length is None:
            max_length = 10
        super().__init__(maxlen=max_length)

        # mutex must be held whenever the queue is mutating.  All methods
        # that acquire mutex must release it before returning.  mutex
        # is shared between the three conditions, so acquiring and
        # releasing the conditions also acquires and releases mutex.
        self.mutex = threading.Lock()

        # Notify not_empty whenever an item is added to the queue; a
        # thread waiting to get is notified then.
        self.not_empty = threading.Condition(self.mutex)

    def put(self, x):
        self.append(x)

    def append(self, x):
        with self.not_empty:
            super().append(x)
            self.not_empty.notify()

    def appendleft(self, x):
        with self.not_empty:
            super().appendleft(x)
            self.not_empty.notify()

    def pop(self, timeout: int = 1):
        with self.not_empty:
            self._block_and_notify(timeout)
            item = super().pop()
            return item

    def popleft(self, timeout: int = 1):
        with self.not_empty:
            self._block_and_notify(timeout)
            item = super().popleft()
            return item

    def _block_and_notify(self, timeout: int or None):
        endtime = time() + timeout
        while not len(self):
            remaining = endtime - time()
            if remaining <= 0.0:
                from queue import Empty
                raise Empty
            self.not_empty.wait(remaining)

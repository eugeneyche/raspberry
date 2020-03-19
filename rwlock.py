import threading
from contextlib import contextmanager


class RwLock(object):
    def __init__(self):
        self._read_ready = threading.Condition(threading.Lock())
        self._readers = 0

    @contextmanager
    def read(self):
        try:
            self._acquire_read()
            yield
        finally:
            self._release_read()

    @contextmanager
    def write(self):
        try:
            self._acquire_write()
            yield
        finally:
            self._release_write()

    def _acquire_read(self):
        self._read_ready.acquire()
        try:
            self._readers += 1
        finally:
            self._read_ready.release()

    def _release_read(self):
        self._read_ready.acquire()
        try:
            self._readers -= 1
            if not self._readers:
                self._read_ready.notifyAll()
        finally:
            self._read_ready.release()

    def _acquire_write(self):
        self._read_ready.acquire()
        while self._readers > 0:
            self._read_ready.wait()

    def _release_write(self):
        self._read_ready.release()  
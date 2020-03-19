from datetime import datetime
import threading
from rwlock import RwLock
from copy import deepcopy
from collections import namedtuple
from timeout import with_timeout


FETCH_TIMEOUT = 15


DataWithVersion = namedtuple("DataWithVersion", ["data", "version"])

class FetchTimeoutError(Exception):
    pass

class InvalidNamespaceError(Exception):
    pass

class NotAtHeadVersionError(Exception):
    pass


class Namespace(object):
    def __init__(self):
        self._data = None
        self._version = 0
        self._version_ready = threading.Condition(threading.Lock())

    def fetch(self, version):
        start_time = datetime.now()
        self._version_ready.acquire()
        try:
            while (self._version == version):
                self._version_ready.wait(5)
                if (datetime.now() - start_time).seconds >= FETCH_TIMEOUT:
                    raise FetchTimeoutError

            current_version = self._version
            data = deepcopy(self._data)
            return DataWithVersion(data=data, version=self._version)
        finally:
            self._version_ready.release()

    def commit(self, version, data):
        self._version_ready.acquire()
        try:
            if self._version != version:
                raise NotAtHeadVersionError
            self._version += 1
            self._data = deepcopy(data)
            # Notify threads blocking for new version
            self._version_ready.notifyAll()
        finally:
            self._version_ready.release()


class State(object):
    _instance = None
    _instance_lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        cls._instance_lock.acquire()
        try:
            if cls._instance is None:
                cls._instance = State()
            return cls._instance
        finally:
            cls._instance_lock.release()

    def __init__(self):
        self._rwlock = RwLock()
        self._namespaces = {}

    def create_namespace(self, name):
        with self._rwlock.write():
            if self._namespaces.get(name) is None:
                self._namespaces[name] = Namespace()
                return True
            else:
                return False
    
    def list_namespaces(self):
        with self._rwlock.read():
            return self._namespaces.keys()

    def commit(self, ns, data, version):
        with self._rwlock.read():
            namespace = self._namespaces.get(ns)
            if namespace is None:
                raise InvalidNamespaceError
            return namespace.commit(data, version)
        
    def fetch(self, ns, version):
        with self._rwlock.read():
            namespace = self._namespaces.get(ns)
            if namespace is None:
                raise InvalidNamespaceError
            return namespace.fetch(version)
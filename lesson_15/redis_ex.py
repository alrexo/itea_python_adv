from abc import ABC, abstractmethod


class BaseBackend(ABC):
    @abstractmethod
    def get_setting(self, name):
        pass

    @abstractmethod
    def set_setting(self, name, value):
        pass


class RedisBackend(BaseBackend):
    import fakeredis
    redis_db = fakeredis.FakeStrictRedis()

    def get_setting(self, name):
        self.redis_db.get(name)

    def set_setting(self, name, value):
        self.redis_db.set(name, value)

    def __setattr__(self, name, value):
        self.set_setting(name, value)


class OSENVBackend(BaseBackend):
    pass


class MongoBackend(BaseBackend):
    from pymongo import MongoClient
    mongo_db = MongoClient()

    def get_setting(self, name):
        pass

    def set_setting(self, name, value):
        pass

    def __setattr__(self, name, value):
        self.set_setting(name, value)


class Env:
    def __init__(self, backend='fakeredis'):
        self.backend = backend
        if self.backend == 'fakeredis':
            self.b = RedisBackend()
        elif self.backend == 'OS_ENV':
            self.b = OSENVBackend()
        elif self.backend == 'Mongo':
            self.b = MongoBackend()

    def __getattr__(self, name):
        self.b.get_setting(name)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)


obj = Env()
print(dir(obj))
print(dir(obj.b))

obj.setting1 = 'bla'
print(obj.setting1)

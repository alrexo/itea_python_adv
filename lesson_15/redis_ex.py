from abc import ABC, abstractmethod
from os import environ
import re


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
        return self.redis_db.get(name)

    def set_setting(self, name, value):
        self.redis_db.set(name, value)

    def __setattr__(self, name, value):
        self.set_setting(name, value)


class OSENVBackend(BaseBackend):

    _BOOL = {'True': True,  'False': False}

    _regex = re.compile("^[-+]?\d+\.\d+$")

    def get_setting(self, name):
        value = environ.get(name, '')

        if value.isdigit():
            return int(value)

        if OSENVBackend._regex.match(value):
            return float(value)

        if value in OSENVBackend._BOOL:
            return OSENVBackend._BOOL[value]

        return value

    def set_setting(self, name, value):
        environ[name] = value

    def __setattr__(self, name, value):
        self.set_setting(name, value)


class MongoBackend(BaseBackend):

    from pymongo import MongoClient

    mongo_db = MongoClient()
    db = mongo_db.test_database
    settings = db.settings

    def get_setting(self, name):
        return self.settings.find_one({'doc_type': 'config'})[name]

    def set_setting(self, name, value):
        self.settings.update_one({'doc_type': 'config'}, {'$set': {name: value}}, upsert=True)

    def __setattr__(self, name, value):
        self.set_setting(name, value)
        print('mongo __setattr__ reached')


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
        return self.b.get_setting(name)

    def __setattr__(self, name, value):
        super().__setattr__(name, value)


# obj_r = Env()
# obj_r.setting1 = 'bla redis'
# print(obj_r.setting1)
#
# obj_os = Env('OS_ENV')
# obj_os.setting1 = 'bla os'
# print(obj_os.setting1)
# print('PYTHONPATH:', obj_os.PYTHONPATH)


obj_mn = Env('Mongo')
print(obj_mn.config_1)
obj_mn.setting1 = 'bla mongo'
print(obj_mn.setting1)

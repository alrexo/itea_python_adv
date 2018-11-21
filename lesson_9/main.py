import arrow


class SingletonFactory:
    __instance = None

    def __init__(self, name):
        self.name = name
        ''' Virtually private constructor. '''
        if SingletonFactory.__instance is not None:
            raise Exception("There's only one factory in the city!")
        else:
            SingletonFactory.__instance = self

    def get_name(self):
        return self.name

    def create_monitor(self, model, diagonal):
        return Monitor(model, diagonal)

    def create_keyboard(self, kb_type):
        return Keyboard(kb_type)

    def create_system_unit(self, su_type):
        return SystemUnit(su_type)


class Computer:
    def __init__(self, monitor, keyboard, system_unit):
        self.monitor = monitor
        self.keyboard = keyboard
        self.system_unit = system_unit


class Monitor:
    def __init__(self, model, diagonal):
        self.date = arrow.utcnow()
        self.vendor = factory.get_name()
        self.model = model
        self.diagonal = diagonal


class Keyboard:
    def __init__(self, kb_type):
        self.date = arrow.utcnow()
        self.vendor = factory.get_name()
        if kb_type == 'PC' or kb_type == 'Bluetooth':
            self.kb_type = kb_type
        else:
            raise Exception('Invalid keyboard type')


class SystemUnit:
    def __init__(self, su_type):
        self.date = arrow.utcnow()
        self.vendor = factory.get_name()
        if su_type == 'Tower' or su_type == 'MiniTower':
            self.su_type = su_type
        else:
            raise Exception('Invalid system unit type')


factory = SingletonFactory('Compus')
su = factory.create_system_unit('Tower')
print(su.date, su.vendor, su.su_type)
factory.name = 'Test'
print(factory.name)
su2 = factory.create_system_unit('Tower')
print(su2.date, su2.vendor, su2.su_type)

# su3 = factory.create_system_unit('Bla')
# print(su3.date, su3.vendor, su3.type)
# factory2 = SingletonFactory('Compus2')

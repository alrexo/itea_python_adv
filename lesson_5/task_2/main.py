class ConstAttributeError(Exception):
    """Custom exception"""

    def __init__(self, message):
        super(ConstAttributeError, self).__init__(message)


class Constant(type):
    """Metaclass that allows creating  classes in which it's unacceptable
    to assign to the fields, but it's clearly possible to do in it's objects"""

    def __setattr__(cls, attr, val):
        raise ConstAttributeError("Assignment to the class's field {}.{} = {}".format(cls, attr, val))


class A(metaclass=Constant):
    x = 1


A().x = 2
try:
    A.x = 2
except ConstAttributeError:
    print('Custom exception works!')

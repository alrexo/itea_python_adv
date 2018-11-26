from abc import ABC, abstractmethod


class ValidationError(AssertionError):
    pass


class NumberBaseContext(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def validate(self, value):
        pass

    @abstractmethod
    def __getattr__(self, item):
        pass

    @abstractmethod
    def __setattr__(self, key, value):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass


class Context(dict, NumberBaseContext):
    def __init__(self, **kwargs):
        """Constructor of the Context class.
        Can take any number of variables"""
        super().__init__()
        if not all(self.validate(v) for k, v in kwargs.items()):
            raise TypeError("Validation error")
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def validate(self, value):
        return isinstance(value, object)

    def __getattr__(self, item):
        """Returns variable's value"""
        return self[item]

    def __setattr__(self, key, value):
        """Sets a value for a variable.
        If the name is invalid, throws NameError"""
        if not self.validate(value):
            raise TypeError("Validation error")
        if not key.isidentifier():
            raise NameError
        self[key] = value

    def __len__(self):
        """Returns number of variables"""
        return len(self.keys())

    def __str__(self):
        """Represents class as a string"""
        return "Class({})".format(", ".join("{}={}".format(k, v) for k, v in self.items()))

    def __iter__(self):
        """Iteration tool"""
        for k, v in self.items():
            yield "{}={}".format(k, v)


class RealContext(Context):
    def __init__(self, **kwargs):
        if not all(self.validate(v) for k, v in kwargs.items()):
            raise TypeError("Given value is not a real number")
        super().__init__(**kwargs)

    def validate(self, value):
        return isinstance(value, (int, float)) or (isinstance(value, complex) and value.imag == 0)

    def __setattr__(self, key, value):
        if not self.validate(value):
            raise TypeError("Given value is not a real number")
        super().__setattr__(key, value)


class ComplexContext(Context):
    def __init__(self, **kwargs):
        if not all(self.validate(v) for k, v in kwargs.items()):
            raise TypeError("Given value is not a complex number")
        super().__init__(**kwargs)

    def validate(self, value):
        return isinstance(value, complex) and value.imag != 0

    def __setattr__(self, key, value):
        if not self.validate(value):
            raise TypeError("Given value is not a complex number")
        super().__setattr__(key, value)


class NumberContext(RealContext, ComplexContext):
    def __init__(self, **kwargs):
        if not all(self.validate(v) for k, v in kwargs.items()):
            raise ValidationError("Given value is not a number")
        super().__init__(**kwargs)

    def validate(self, value):
        return RealContext().validate(value) or ComplexContext().validate(value)

    def __setattr__(self, key, value):
        if not self.validate(value):
            raise TypeError("Given value is not a number")
        super().__setattr__(key, value)


inr = 5
flt = 8.5
com = 20j

real = RealContext()
real.inr = inr
print(real.inr)
real.flt = flt
print(real.flt)
try:
    real.com = com
except TypeError as e:
    print(com, repr(e))

comp = ComplexContext()
comp.com = com
print(comp.com)
try:
    comp.inr = 20
except TypeError as e:
    print(inr, repr(e))

num = NumberContext()
num.inr = inr
num.flt = flt
num.com = com
print(num.inr, num.flt, num.com)

class Context(dict):
    def __init__(self, **kwargs):
        """Constructor of the Context class.
        Can take any number of variables"""
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __getattr__(self, item):
        """Returns variable's value"""
        return self[item]

    def __setattr__(self, key, value):
        """Sets a value for a variable.
        If the name is invalid, throws NameError"""
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


obj = Context(a=1, b=2)
obj.c8 = 31
obj.d15 = 33

print(obj)
print(len(obj))

for i in obj:
    print(i)

class Context(dict):
    def __init__(self, **kwargs):
        super().__init__()
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

    def __enter__(self):
        for k, v in self.items():
            globals()[k] = v

    def __exit__(self, exc_type, exc_val, exc_trace):
        for k, v in self.items():
            del globals()[k]


x, y, z = 10, 20j, "Hello world"
print(x, y, z)

with Context(x=1, y=2j, z="Hello") as c:
    print(x, y, z)

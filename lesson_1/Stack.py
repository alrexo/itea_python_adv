class LimitExceedError(Exception):
    pass


class Stack:
    def __init__(self, data_type=object, limit=None):
        self.data_type = data_type
        self.limit = limit
        if limit is None:
            self.stack = []
        else:
            self.stack = [None for i in range(self.limit)]

    def _push(self, element):
        """Checks if it's possible to add the element to the stack.
        Throws TypeError if element's type mismatches self.data_type.
        Throws LimitExceedError if the stack is full."""
        if not isinstance(element, self.data_type):
            raise TypeError("The stack doesn't support this type")
        elif self.limit is None:
            return True
        elif self.count() >= self.limit:
            raise LimitExceedError("The stack is full")
        else:
            return True

    def push(self, element):
        """Adds element to the stack"""
        if self._push(element) and self.count() == len(self.stack) and self.limit is None:
            self.stack.append(element)
            return
        if self._push(element):
            self.stack[self.count()] = element

    def pull(self):
        """Returns last non-None element from the stack"""
        if self.count():
            return self.stack[self.count() - 1]

    def count(self):
        """Counts non-None elements in self.stack"""
        count = 0
        for i in self.stack:
            if i is not None:
                count += 1
        return count

    def clear(self):
        """Clears the stack"""
        for i in range(self.limit):
            self.stack[i] = None

    @property
    def type(self):
        """Returns string representation of stack type"""
        return self.data_type.__name__

    def __str__(self):
        """Returns info about stack's type"""
        return "Stack<{}>".format(self.type)


# Sample tests
unlimited_stack = Stack(int)
print('stack object:', unlimited_stack)
for i in range(20):
    unlimited_stack.push(i)
print('stack content:', unlimited_stack.stack)
try:
    unlimited_stack.push('str')
except TypeError as e:
    print(repr(e), 'Type exception works.')
print('-' * 100)

int_stack = Stack(int, 5)
print('stack object:', int_stack)
int_stack.push(1)
int_stack.push(2)
int_stack.push(3)
int_stack.push(4)
try:
    int_stack.push('str')
except TypeError as e:
    print(repr(e), 'Type exception works.')
int_stack.push(5)
try:
    int_stack.push(6)
except LimitExceedError as e:
    print(repr(e), 'Custom exception works.')
print('stack content:', int_stack.stack)
print('stack length:', int_stack.count())
print('last element:', int_stack.pull())
int_stack.clear()
print('stack content:', int_stack.stack)
print('stack length:', int_stack.count())
print('-' * 100)

str_stack = Stack(str, 3)
print('stack object:', str_stack)
str_stack.push('abc')
str_stack.push('xyz')
str_stack.push('xxx')
print('stack content:', str_stack.stack)
print('stack length:', str_stack.count())
print('last element:', str_stack.pull())
str_stack.clear()
print('stack content:', str_stack.stack)
print('stack length:', str_stack.count())
print('-' * 100)

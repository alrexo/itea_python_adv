import os
import sys


class LogReader:
    def __init__(self, mask='.log', path=sys.path[0]):
        self.path = path
        self.mask = mask

    @property
    def files(self):
        return [i for i in os.listdir(self.path) if i.endswith(self.mask)]

    def __iter__(self):
        for file in self.files:
            with open(file) as f:
                for line in f:
                    yield line.rstrip('\n')


log_reader = LogReader()
for i in log_reader:
    print(i)
print(log_reader.files)

print('-' * 30)

txt_reader = LogReader('.txt')
for i in txt_reader:
    print(i)
print(txt_reader.files)

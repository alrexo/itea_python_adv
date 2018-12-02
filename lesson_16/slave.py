import sys


def check_params():
    if len(sys.argv) == 4:
        try:
            global start, end, step
            start, end, step = map(int, sys.argv[1:4])
        except ValueError:
            print('Invalid parameter(s)! Integers only.')
            exit(0)
    else:
        print('Wrong number of parameters!')
        exit(0)


def thread_func(start, end, step):
    s = sum((i for i in range(start, end + 1, step)))
    print(s)


if __name__ == '__main__':
    check_params()
    thread_func(start, end, step)

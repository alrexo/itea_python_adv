import random
import subprocess
from multiprocessing import Pool


def get_random_params():
    start = random.randint(0, 100)
    end = random.randint(start + 100, start + 100 + random.randint(0, 100))
    step = random.randint(1, 5)
    output = (start, end, step)
    return output


def seq_sum(args):
    start, end, step = args
    process = subprocess.Popen('python slave.py {} {} {}'.format(start, end, step))
    while process.poll() is None:
        pass
    print('pid =', process.pid)


def parallel_runs(procs):
    with Pool(procs) as pool:
        pool.map(seq_sum, params)


if __name__ == '__main__':
    number_of_processes = 3
    params = (get_random_params() for i in range(number_of_processes))
    parallel_runs(number_of_processes)

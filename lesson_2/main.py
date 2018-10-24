from time import sleep
from monitor import monitor

input_dir = r'C:\Users\Alexo\PycharmProjects\ITEA_Python_Adv\Homework\lesson_2\Input'
output_dir = r'C:\Users\Alexo\PycharmProjects\ITEA_Python_Adv\Homework\lesson_2\Output'
error_dir = r'C:\Users\Alexo\PycharmProjects\ITEA_Python_Adv\Homework\lesson_2\Errors'

while True:
    monitor(input_dir, output_dir, error_dir)
    sleep(5)

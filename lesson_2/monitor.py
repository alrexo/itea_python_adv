"""This module contains monitor() and process() functions. It also has a function decorator.
Map() function is used in process() function.
"""

import os
from datetime import datetime

from file_processing import process_valid_file, copy_error_file


def duration_logger(original_function):
    """Function decorator which measures execution time of the wrapped function and
    displays the time with the function's name.

    Args:
        original_function (function): The function to measure.

    Returns:
        function: Wrapper function definition.
    """

    def wrapper_function(*args, **kwargs):
        start_time = datetime.utcnow()
        output = original_function(*args, **kwargs)
        duration = str(datetime.utcnow() - start_time)
        print('Executed function:', original_function.__name__, '; Duration:', duration, '\n')
        return output

    return wrapper_function


@duration_logger
def process(file_path):
    """The function opens a file and checks whether the file is not empty and contains valid content
    (a string with Python's list). Valid content is summed up, otherwise an error message is captured.

    Args:
        file_path (str): The path to the file to read and to validate.

    Returns:
        dict: Dictionary with validation and data processing results.
    """
    output = {}
    with open(file_path, 'r') as f:
        if os.stat(file_path).st_size == 0:
            output['Error'] = 'Empty file'
        elif len(f.readlines()) > 1:
            output['Error'] = 'Invalid file (multiple lines)'
        f.seek(0)
        line = f.read().replace(" ", "").rstrip()
        if line.startswith('[') and line.endswith(']'):
            try:
                input_list = map(int, line[1:-1].split(','))
                output['Valid Content'] = str(sum(input_list))
            except ValueError:
                output['Error'] = 'Invalid content'
    return output


def monitor(input_dir, output_dir, error_dir):
    """The function looks for .txt files in the input directory, reads and validates them (via process() function).
    Valid content is written in new files in the output directory. All other files are moved to the error directory.
    All processed files are removed from the input folder. All program runs are logged in the output directory.

    Args:
        input_dir (str): Input directory path.
        output_dir (str): Output directory path.
        error_dir (str): Error directory path.

    Returns:
        dict: Dictionary with validation and data processing results.
    """
    start_time = datetime.utcnow()
    count = 0
    for file_name in os.listdir(input_dir):
        input_file_path = os.path.join(input_dir, file_name)
        if file_name.endswith('.txt'):
            read_result = process(input_file_path)
            if 'Valid Content' in read_result:
                process_valid_file(input_file_path, output_dir, read_result['Valid Content'])
            else:
                copy_error_file(input_file_path, error_dir, str(read_result))
        else:
            copy_error_file(input_file_path, error_dir, "'{'Error': 'Not a txt file'}'")
        os.remove(input_file_path)
        count += 1
    with open(os.path.join(output_dir, 'run_log.txt'), 'a+') as log:
        log.write('Program started at: ' + start_time.strftime('%Y-%m-%d %H:%M:%S')
                  + '; finished at: ' + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                  + '; processed files: ' + str(count) + '\n')

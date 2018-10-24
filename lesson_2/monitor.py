import os
from datetime import datetime

from file_processing import process_valid_file, copy_error_file


def duration_logger(original_function):
    def wrapper_function(*args, **kwargs):
        start_time = datetime.utcnow()
        output = original_function(*args, **kwargs)
        duration = str(datetime.utcnow() - start_time)
        print('Executed function:', original_function.__name__, '; Duration:', duration, '\n')
        return output

    return wrapper_function


@duration_logger
def process(file_path):
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

import os
from datetime import datetime
from shutil import copyfile


def create_file(file_path):
    try:
        with open(file_path, 'x') as f:
            pass
    except FileExistsError:
        file_name, file_extension = os.path.splitext(os.path.basename(file_path))
        file_path = os.path.join(os.path.dirname(file_path),
                                 file_name + '_' + datetime.utcnow().strftime('%Y%m%d%H%M%S') + file_extension)
        with open(file_path, 'x') as f:
            pass
    finally:
        return file_path


def process_valid_file(input_file_path, output_dir, result):
    output_file_path = create_file(os.path.join(output_dir, os.path.basename(input_file_path)))
    with open(output_file_path, 'w') as output_file:
        output_file.write(result)
    with open(os.path.join(output_dir, 'output_log.txt'), 'a+') as log:
        log.write(datetime.utcnow().strftime('[%Y-%m-%d %H:%M:%S] Output file name: ')
                  + os.path.basename(output_file_path)
                  + '; Input file name: ' + os.path.basename(input_file_path)
                  + '; Last modification date: '
                  + datetime.utcfromtimestamp(os.path.getmtime(input_file_path)).strftime('%Y-%m-%d %H:%M:%S')
                  + '\n')


def copy_error_file(input_file_path, error_dir, error_message):
    error_file_path = create_file(os.path.join(error_dir, os.path.basename(input_file_path)))
    with open(os.path.join(error_dir, 'errors_log.txt'), 'a+') as log:
        log.write(datetime.utcnow().strftime('[%Y-%m-%d %H:%M:%S] ') + os.path.basename(error_file_path) +
                  ' ' + error_message + '\n')
    copyfile(input_file_path, error_file_path)

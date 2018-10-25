"""This module contains the functions for file processing:
    - create_file
    - process_valid_file
    - copy_error_file
"""

import os
from datetime import datetime
from shutil import copyfile


def create_file(file_path):
    """The function creates an empty shell file with a given file path if it doesn't exist. If the file already exists,
    the function adds a UTC timestamp (up to seconds) to the name of the newly created file.

    Args:
        file_path (str): The path of the file to be created.

    Returns:
        str: The path of the created file.
    """
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


def process_valid_file(input_file_path, output_dir, data):
    """The function reads the file name from input_file_path, creates a target file with the same name (or timestamp
    suffix) in the output directory and writes the given data to it. File processing is logged in the output directory.

    Args:
        input_file_path (str): The path of the input file to be processed.
        output_dir (str): Output directory.
        data (str): Data to be written into the output file.
    """
    output_file_path = create_file(os.path.join(output_dir, os.path.basename(input_file_path)))
    with open(output_file_path, 'w') as output_file:
        output_file.write(data)
    with open(os.path.join(output_dir, 'output_log.txt'), 'a+') as log:
        log.write(datetime.utcnow().strftime('[%Y-%m-%d %H:%M:%S] Output file name: ')
                  + os.path.basename(output_file_path)
                  + '; Input file name: ' + os.path.basename(input_file_path)
                  + '; Last modification date: '
                  + datetime.utcfromtimestamp(os.path.getmtime(input_file_path)).strftime('%Y-%m-%d %H:%M:%S') + '\n')


def copy_error_file(input_file_path, error_dir, error_message):
    """The function reads the file name from input_file_path, creates a target file with the same name (or timestamp
    suffix) in the error directory. Then it copies the input file to the error directory.
    File processing is logged in the error directory.

    Args:
        input_file_path (str): The path of the input file to be copied.
        error_dir (str): Error directory.
        error_message (str): Error message for the log file.
    """
    error_file_path = create_file(os.path.join(error_dir, os.path.basename(input_file_path)))
    with open(os.path.join(error_dir, 'errors_log.txt'), 'a+') as log:
        log.write(datetime.utcnow().strftime('[%Y-%m-%d %H:%M:%S] ') + os.path.basename(error_file_path)
                  + ' ' + error_message
                  + '; Input file name: ' + os.path.basename(input_file_path)
                  + '; Last modification date: '
                  + datetime.utcfromtimestamp(os.path.getmtime(input_file_path)).strftime('%Y-%m-%d %H:%M:%S') + '\n')
    copyfile(input_file_path, error_file_path)

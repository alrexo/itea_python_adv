"""This module reverses character by character the content of a file passed in the command line, otherwise the built-in
test file is created and reversed.
"""
import os
import sys


def create_test_file():
    """The function creates a test file with one-byte and two-bytes characters as well various types of newlines.
    """
    with open('test.txt', 'w', encoding='utf8', newline='') as tf:
        tf.write('123456789')
        tf.write('abcd')
        tf.write('\r')
        tf.write('äöüß')
        tf.write('\n')
        tf.write('абвг')
        tf.write('\r\n')
        tf.write('+#&$@°^')
        tf.write('\n\n')
        tf.write('end')


def reverse_txt_file(file_path):
    """The function reverses character by character the content of a file passed as the argument. The logic: firstly,
    bytes length of the file is determined, then, each character is read backwards from the end of the file and is
    appended to the end of the file. Once the reversed string has been completely written, the original content
    (that is, everything before bytes length) is overwritten by the reversed string. Finally, the tail of the file is
    truncated. To disable python's automatic newline conversion, open is called with newline='' parameter.

    Args:
        file_path (str): The path of the file to reverse.
    """
    with open(file_path, 'r+', encoding='utf8', newline='') as f:
        # save the original state of the file for testing purposes
        original_state = repr(f.read()); print('Original state:', original_state)
        # start of the actual code
        f.seek(0, 2)
        bytes_length = f.tell()
        print('bytes_length =', bytes_length)
        # Reading characters backwards and appending them to the end of the file. '\r\n' stays '\r\n'.
        processed_bytes = 0
        processed_chars = 0
        previous_char = None
        while processed_bytes < bytes_length:
            position = bytes_length - 1 - processed_bytes
            f.seek(position)
            try:
                char = f.read(1)
            except UnicodeDecodeError:
                f.seek(position - 1)
                char = f.read(1)
            f.seek(0, 2)
            if previous_char == '\n':
                if char == '\r':
                    f.write(char + previous_char)  # '\r\n'
                else:
                    f.write(previous_char + char)
            elif char != '\n':
                f.write(char)
            if previous_char == '\n' and char == '\n':
                previous_char = None
            else:
                previous_char = char[:]
            processed_bytes += len(char.encode('utf8'))
            # demonstration for testing purposes
            processed_chars += len(char)
            print(str(position).zfill(2), str(processed_chars).zfill(2), str(processed_bytes).zfill(2),
                  repr(char).ljust(4), len(char.encode('utf8')))
        # Overwriting the beginning of the file by the appended characters and truncating the appendix at the end.
        processed_bytes = 0
        processed_chars = 0
        while processed_bytes < bytes_length:
            position = bytes_length - 0 + processed_bytes
            f.seek(position)
            char = f.read(1)
            f.seek(processed_bytes)
            f.write(char)
            processed_bytes += len(char.encode('utf8'))
            # demonstration for testing purposes
            processed_chars += len(char)
            print(str(position).zfill(2), str(processed_chars).zfill(2), str(processed_bytes).zfill(2),
                  repr(char).ljust(4), len(char.encode('utf8')))
        f.truncate()
        # demonstration for testing purposes
        f.seek(0); print('Was:', original_state, '\n', 'Is:', repr(f.read()))


if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
        reverse_txt_file(file_path)
    except IndexError:
        print('File to reverse is not defined! Proceeding with a test file.')
    except FileNotFoundError:
        print('File to reverse not found! Proceeding with a test file.')
    finally:
        create_test_file()
        file_path = os.path.join(os.getcwd(), 'test.txt')
        reverse_txt_file(file_path)

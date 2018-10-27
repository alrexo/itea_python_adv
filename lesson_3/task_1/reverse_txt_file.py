n = open('test.txt', 'w', encoding='utf8', newline='')
n.write('123456789')
n.write('abcd')
n.write('\r')
n.write('äöüß')
n.write('\n')
n.write('абвг')
n.write('\r\n')
n.write('+#&$@°^')
n.write('\n\n')
n.write('end')
n.close()


def reverse_txt_file(file_path):
    with open(file_path, 'r+', encoding='utf8', newline='') as f:
        # save the original state of the file for testing purposes
        original_state = repr(f.read()); print(original_state)
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
                  repr(char).ljust(4),
                  len(char.encode('utf8')))
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
                  repr(char).ljust(4),
                  len(char.encode('utf8')))
        f.truncate()
        # demonstration for testing purposes
        f.seek(0); print('Was:', original_state, '\n', 'Is:', repr(f.read()))


reverse_txt_file(r'C:\Users\Alexo\PycharmProjects\ITEA_Python_Adv\Homework\lesson_3\task_1\test.txt')

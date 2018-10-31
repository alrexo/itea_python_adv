import csv
import json
import pickle
import re
import shelve

import xlrd
from exceptions import InvalidUsernameError, InvalidEmailError, InvalidDateError, NoValueError


class FileConverter:
    username_x_pattern = re.compile(r'[^a-zA-Z]')
    email_in_pattern = re.compile(r'(^[a-zA-Z_.]+@[a-zA-Z]+(\.[a-zA-Z]+){1,2}$)')
    date_in_pattern = re.compile(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))')

    def __init__(self, file_location):
        self.file_location = file_location
        self.valid_data = []
        self.invalid_data = []

    def read_workbook(self):
        workbook = xlrd.open_workbook(self.file_location)
        sheet = workbook.sheet_by_index(0)
        header = []
        users_data = []
        n_cols = 3  # sheet.ncols
        for row in range(sheet.nrows):
            if row == 0:
                for col in range(n_cols):
                    header.append(sheet.cell_value(row, col))
            else:
                user = dict()
                for col in range(n_cols):
                    user[header[col]] = sheet.cell_value(row, col)
                users_data.append(user.copy())
        return users_data

    def validate_username(self, username):
        return not bool(self.username_x_pattern.search(username))

    def validate_email(self, email):
        return bool(re.fullmatch(self.email_in_pattern, email))

    def validate_date(self, date_string):
        try:
            result = bool(re.fullmatch(self.date_in_pattern, date_string))
        except TypeError:
            result = False
        return result

    @staticmethod
    def convert_date(date_string):
        yyyy, mm, dd = date_string.split('-')
        return mm + '/' + dd + '/' + yyyy

    def process_data(self, data):
        valid_users_data = []
        invalid_users_data = []
        for user in data:
            try:
                if '' in user.values():
                    raise NoValueError
                if not self.validate_username(user['Username']):
                    raise InvalidUsernameError
                if not self.validate_email(user['Email']):
                    raise InvalidEmailError
                if not self.validate_date(user['Joined']):
                    raise InvalidDateError
                user['Joined'] = self.convert_date(user['Joined'])
                valid_users_data.append(user.copy())
            except (NoValueError, InvalidUsernameError, InvalidEmailError, InvalidDateError):
                invalid_users_data.append(user.copy())
        processed_data = dict()
        processed_data['Valid'] = valid_users_data
        processed_data['Errors'] = invalid_users_data
        return processed_data

    @staticmethod
    def export_to_csv(data):
        with open('output.csv', 'w', newline='') as csvfile:
            fieldnames = data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for element in data:
                writer.writerow(element)

    @staticmethod
    def export_to_json(data):
        json_data = json.dumps(data, indent=4)
        with open('output.json', 'w') as f:
            f.write(json_data)

    @staticmethod
    def export_to_bin(data):
        bin_data = pickle.dumps(data)
        with open('output.bin', 'wb') as f:
            f.write(bin_data)

    @staticmethod
    def export_to_shelf(data_dict):
        with shelve.open('output', 'c') as shelf:
            for key in data_dict.keys():
                shelf[key] = data_dict[key]

    @staticmethod
    def export_errors(data):
        with open('errors.log', 'w') as f:
            f.write(str(data))
            # f.write(str([list(line.values()) for line in data]))

    def convert(self):
        workbook_data = self.read_workbook()
        processed_data = self.process_data(workbook_data)
        self.valid_data = processed_data['Valid']
        self.invalid_data = processed_data['Errors']

    def export(self):
        self.export_to_csv(self.valid_data)
        self.export_to_json(self.valid_data)
        self.export_to_bin(self.valid_data)
        self.export_to_shelf(dict(Valid=self.valid_data))
        self.export_errors(self.invalid_data)


file_location = r'C:\Users\Alexo\PycharmProjects\ITEA_Python_Adv\Homework\lesson_3\task_2\Test.xlsx'
f = FileConverter(file_location)
f.convert()
f.export()

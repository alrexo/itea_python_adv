class InvalidFormat(Exception):
    pass


class InvalidIdentifier(Exception):
    pass


class InvalidValue(Exception):
    pass


name_of_class = input('Enter class name: ')
class_fields = {}
while True:
    inp = input('Enter class fields as "N=V": ')
    if inp == '':
        print('Thank you! Your input has been recorded.')
        print('-' * 100)
        break
    else:
        try:
            if '=' not in inp:
                raise InvalidFormat('Invalid format!')
            var_list = inp.split('=')
            field_name, field_value = var_list[0].strip(), var_list[1].lstrip()
        except InvalidFormat:
            print('Invalid format!')
            continue
        try:
            if not field_name.isidentifier():
                raise InvalidIdentifier('Invalid Identifier!')
        except InvalidIdentifier:
            print('Invalid Identifier!')
            continue
        try:
            if field_value.upper() in ['TRUE', 'FALSE']:
                class_fields[field_name] = bool(field_value)
            elif (field_value.startswith("'") and field_value.endswith("'")) or (
                    field_value.startswith('"') and field_value.endswith('"')):
                class_fields[field_name] = field_value
            else:
                try:
                    int(field_value)
                    class_fields[field_name] = int(field_value)
                except ValueError:
                    raise InvalidValue('InvalidValue')
        except InvalidValue:
            print('Invalid Value!')
            continue


# Creating a class with entered class fields
MyClass = type(name_of_class, (object,), class_fields)

# Creating an object of class A
ob = MyClass()

print(MyClass)
# print(ob)
# print(ob.__class__.__name__)
# print('MyClass dict:', MyClass.__dict__)
# print('Object dict:', ob.__dict__)
# print('Object dir:', dir(ob))

for attr in dir(ob):
    if not attr.startswith('__'):
        print(attr + ':', MyClass.__dict__[attr], type(MyClass.__dict__[attr]))

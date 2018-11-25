import re

regex = (r'(\b' +
            # subgroup: looks for either ip address, domain name or localhost
            r'(' +
                # ip address
                r'\b' +
                r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.' +
                r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.' +
                r'(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.' +
                r'(25[0-4]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])' +
                r'\b' +
            r'|' +
                # domain name
                r'\b(([a-zA-Z0-9]+([-]{1}|[-]{3})[a-zA-Z0-9]+)|[a-zA-Z]+)(\.[a-zA-Z0-9]+)+\b' +
            r'|' +
                # localhost
                r'localhost' +
            r'){1}' +
            # optional subgorup for port number (max 65535)
            r'(' +
                r'\b\:(6553[0-5]|655[0-2][0-9]|65[0-4][0-9][0-9]|6[0-4][0-9][0-9][0-9]|' +
                r'[1-5][0-9][0-9][0-9][0-9]|[1-9][0-9][0-9][0-9]|[1-9][0-9][0-9]|[1-9][0-9]|[1-9])\b' +
            r')?' +
         r'\b)')

test_str = ([
    'localhost:5000',
    '127.0.0.1:5000',
    '12.44.33.254:9800',
    '127.0.0.1',
    '127.0.0.254',
    '127.0.0.255',
    'g-mail.com:65535'])

match_list = list(filter(lambda x: x is not None, map(lambda x: re.search(regex, x), test_str)))
print('Full address'.ljust(30, ' '), 'Host'.ljust(25, ' '), 'Port')
print('-'*30, '-'*25, '-'*5)
for match in match_list:
    print(match.group(1).ljust(30, ' '), match.group(2).ljust(25, ' '),
          '' if match.group(12) is None else match.group(12))

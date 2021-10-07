# Progress Functions
# Berkay MIZRAK
# www.BerkayMizrak.com
# www.DaktiNetwork.com

try:
    import time
    from datetime import datetime

    import decimal

    from Functions import Progress
except Exception as e:
    print()
    print(e)
    while True:
        input('\n! ! ERROR --> A module is not installed...')


class colors:
    HEADER = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    DEF = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
# print(bcolors.GREEN + "[+] Online Proxy: " + bcolors.BOLD + str(55) + bcolors.ENDC + "\n")


def from_string_to_type(value, val_type):
    # val_type:
    # try_all
    # str
    # int
    # float
    # datetime_%Y.%m.%d %H:%M
    # bool

    count = 0
    type_list = ['int', 'float', 'bool', 'str']
    test_value = None
    while True:
        if val_type == 'try_all':
            if count == len(type_list):
                break
            test_val_type = type_list[count]
        else:
            if count == 1:
                break
            test_val_type = val_type

        if test_value:
            break
        test_value = value

        try:
            if test_val_type == 'str':
                test_value = str(test_value)
            elif test_val_type == 'int':
                test_value = int(test_value)
            elif test_val_type == 'float':
                test_value = float(test_value)
            elif 'datetime_' in test_val_type:  # datetime_%Y.%m.%d
                test_val_type = test_val_type.replace('datetime_', '')
                test_value = datetime.strptime(test_value, test_val_type)
            elif test_val_type == 'bool':
                if str(test_value).lower() == 'true':
                    test_value = True
                elif str(test_value).lower() == 'false':
                    test_value = False
                    if val_type == 'try_all':
                        break
                elif str(test_value).lower() == 'none':
                    test_value = None
                    if val_type == 'try_all':
                        break
                else:
                    test_value = None
        except:
            test_value = None

        count += 1

    return test_value


# This function helps me to name files I create by my automation apps

def timestamp_def(seperate=False, exit_all=True, alternative='timestamp_error', with_space=False):
    try:
        now_date = datetime.now()
        date = now_date.strftime("%Y.%m.%d")
        hour = now_date.strftime("%H.%M.%S")
        if with_space:
            now = date + ' - ' + hour
        else:
            now = date + '-' + hour

    except Exception as e:
        message = "--> An error occurred while creating timestamp."
        Progress.exit_app(message=message, e=e, exit_all=exit_all)
        now = alternative
        date = alternative
        hour = alternative

    if seperate:
        return date, hour
    else:
        return now

def create_uniq_number(length_of_it=3):
    now = str(time.time())
    unique_id = now[-length_of_it:]
    return unique_id

# Turkish characters for below functions.
rep = [
    ('İ', 'i'),
    ('Ğ', 'ğ'),
    ('Ü', 'ü'),
    ('Ş', 'ş'),
    ('Ö', 'ö'),
    ('Ç', 'ç'),
    ('I', 'ı')
]

# Upper function for Turkish words.
def upper_string(string):
    for replace, search in rep:
        string = string.replace(search, replace)
    return string.upper()

# Lower function for Turkish words.
def lower_string(string):
    for search, replace in rep:
        string = string.replace(search, replace)
    return string.lower()

# Title function for Turkish words.
def title_string(string):
    string = lower_string(string=string)

    words = string.split(' ')
    word_list = list()
    for word in words:
        for search, replace in rep:
            if word.startswith(replace):
                word = search + word[1:]
        word = word.title()
        word_list.append(word)

    string = word_list[0]
    for word in word_list[1:]:
        string = string + ' ' + word
    return string

# Replace last character matched in string.
def replace_last_occurrence(s, old, new):
    return (s[::-1].replace(old[::-1], new[::-1], 1))[::-1]

# Convert number format of date to normal date format.
def date_number_to_date(number):
    date = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + number - 2)
    date = str(date.date())
    date_list = date.split('-')
    full_date = '%s.%s.%s' % (date_list[2], date_list[1], date_list[0])
    return full_date
# USAGE OF NUMBER TO DATE -----------------------
"""
number = 34908
date = date_number_to_date(number)
"""
# USAGE OF NUMBER TO DATE -----------------------


# if force_number, try to make it integer or float.
# If float, check number of decimal and
# 1) if decimal is 0 make it integer.
# 2) if decimal has 1 or 2 numbers, make it float.
# 3) if decimal has more than 2 numbers, make it float and round it to 2 decimals.
# if the input is string with characters which is not number, returns same string.
def float_to_integer(number, force_number=True):
    if force_number:
        if isinstance(number, str):
            try:
                number = float(number)
                number = round(number, 2)
            except:
                pass
        if isinstance(number, str):
            try:
                number = int(number)
            except:
                pass

    if isinstance(number, float):
        d = decimal.Decimal(str(number))
        number_of_dec = -d.as_tuple().exponent
        number_dec = str(abs(number - int(number)))[2:]

        try:
            number_dec = int(number_dec)
        except:
            pass

        if not number_dec:
            number = int(number)
        else:
            if number_of_dec == 1:
                number = round(number, 1)
            else:
                number = round(number, 2)

    return number

"""
items = 'lastPrice', 'change', 'pChange', 'net_oi', 'trend', 'net_change_oi',
if all(i in main_string for i in items):
"""
from datetime import datetime


def get_value_from_user(name):
    """
    Function to get user input

    :param name: name of value
    :return: name
    """
    username = input(f'Enter a value for {name}:')
    return username


def create_date(date_string):
    """
    Function to return a datetime object of the required format
    :param date_string: string to be used
    :return: datetime of format 'YYYY-MM-DD'
    """
    return datetime.strptime(date_string, '%Y-%m-%d')


def has_expected_date_format(date_str):
    """
    Checks that the string used is as expected i.e. YYYY-MM-DD

    :param date_str: string representing date
    :return: True if string is formatted as expected, False otherwise
    """
    if len(date_str) != 10:
        return False
    has_expected_format = True
    try:
        create_date(date_str)
    except ValueError:
        has_expected_format = False
    return has_expected_format


def rreplace(s, old, new, occurrence):
    """
    Function to replace parts of string from right
    :param s: string
    :param old: substring to replace
    :param new: replacement substring
    :param occurrence: no of replacements
    :return: string with replacements

    e.g. rreplace('this is it.', 'i', 'REP', 2) = 'this REPs REPt.'
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)

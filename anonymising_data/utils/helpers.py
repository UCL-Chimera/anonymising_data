from datetime import datetime


YEAR_SLASH, DAY_SLASH, YEAR_DASH, DAY_DASH = range(4)


def create_date(date_string):
    """
    Function to return a datetime object of the required format.

    :param date_string: string to be used
    :return: datetime of format 'YYYY-MM-DD'
    """
    try:
        d = datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        try:
            d = datetime.strptime(date_string, '%d-%m-%Y')
        except ValueError:
            try:
                d = datetime.strptime(date_string, '%Y/%m/%d')
            except ValueError:
                d = datetime.strptime(date_string, '%d/%m/%Y')
    return d


def has_expected_date_format(date_str):
    """
    Checks that the string used is as expected i.e. YYYY-MM-DD.

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
    Function to replace parts of string from right.

    :param s: string
    :param old: substring to replace
    :param new: replacement substring
    :param occurrence: no of replacements
    :return: string with replacements

    e.g. rreplace('this is it.', 'i', 'REP', 2) = 'this REPs REPt.'
    """
    li = s.rsplit(old, occurrence)
    return new.join(li)


def determine_date_format(date_str):
    """
    Function to determine format of a date string.

    Formats are:
    YEAR_SLASH YYYY/MM/DD
    DAY_SLASH  DD/MM/YYYY
    YEAR_DASH  YYYY-MM-DD
    DAY_DASH   DD-MM-YYYY

    :param date_str: date as string
    :return: format of string
    """
    if date_str[0:4].isnumeric():
        if date_str[4] == '/':
            date_format = YEAR_SLASH
        else:
            date_format = YEAR_DASH
    else:
        if date_str[2] == '/':
            date_format = DAY_SLASH
        else:
            date_format = DAY_DASH
    return date_format

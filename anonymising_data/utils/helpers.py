from datetime import datetime


YEAR_SLASH, DAY_SLASH, YEAR_DASH, DAY_DASH, YEAR_COLON = range(5)


def parse_date(date_string):
    formats_to_check = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%d/%m/%Y",
        "%Y:%m:%d",
        "%d.%m.%Y",
        "%m.%d.%Y",
    ]

    for date_format in formats_to_check:
        try:
            d = datetime.strptime(date_string, date_format)
            return d
        except ValueError:
            pass

    return None


def create_date(date_string):
    """
    Function to return a datetime object of the required format
    :param date_string: string to be used
    :return: datetime of format 'YYYY-MM-DD'
    """
    # check for a date surrounded by "
    if date_string.startswith('"'):
        date_string = date_string[1:11]
    else:
        date_string = date_string[0:10]

    # Use the parse_date function
    d = parse_date(date_string)

    if not d:
        print("Date format not recognized:", date_string)

    return d


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


def determine_date_format(date_str):
    """
    Determines the format of a date string.

    :param date_str:
    :return: format
    YEAR_SLASH  yyyy/mm/dd,
    DAY_SLASH   dd/mm/yyyy,
    YEAR_DASH   yyyy-mm-dd,
    DAY_DASH    dd-mm-yyyy,
    YEAR_COLON  yyyy:mm:dd

    """
    if date_str[0:4].isnumeric():
        if date_str[4] == "/":
            date_format = YEAR_SLASH
        elif date_str[4] == "-":
            date_format = YEAR_DASH
        else:
            date_format = YEAR_COLON
    else:
        if date_str[2] == "/":
            date_format = DAY_SLASH
        else:
            date_format = DAY_DASH
    return date_format

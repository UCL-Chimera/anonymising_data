from datetime import datetime


class FileManager:
    """
    Class to manage read from and write to files
    """
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # note might we want to save and flush
        self.file.close()


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

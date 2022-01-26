

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


def is_leap_year(year):
    """
    Predicate indicating that a year is a leap year of not
    :param year: year
    :return: True if leap year, False otherwise
    """
    # divided by 100 means century year (ending with 00)
    # century year divided by 400 is leap year
    if (year % 400 == 0) and (year % 100 == 0):
        return True
    # not a century year divided by 4 is a leap year
    elif (year % 4 == 0) and (year % 100 != 0):
        return True
    else:
        return False

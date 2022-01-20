

class FileManager:
    """
    Class to manage read and write from files
    """
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()


def get_value_from_user(name):
    """
    Function to get user input

    :param name: name of value
    :return: name
    """
    username = input(f'Enter a value for {name}:')
    return username

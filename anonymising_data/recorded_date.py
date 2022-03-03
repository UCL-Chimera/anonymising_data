from datetime import datetime, timedelta


class RecordedDate:
    """
    Class to shift the date and time by prescribed amount
    """
    def __init__(self, original):
        self.original = original
        self.offset = 0
        self.shifted_date = original

    @property
    def original(self):
        """
        Function to retrieve the original date
        :return: _original_date
        """
        return self._original

    @original.setter
    def original(self, value):
        """
        Function to set the original date
        """
        self._original = datetime.strptime(value, '%Y-%m-%d')
        print('ss')

    @property
    def shifted_date(self):
        """
        Function to retrieve the shifted date
        :return: _shifted_date
        """
        return self._shifted_date

    @shifted_date.setter
    def shifted_date(self, value):
        """
        Function to set the shifted date
        """
        self._shifted_date = datetime.strptime(value, '%Y-%m-%d')

    @property
    def offset(self):
        """
        Function to retrieve the offset period
        :return: _offset
        """
        return self._offset

    @offset.setter
    def offset(self, value):
        """
        Function to set the offset period in days
        """
        self._offset = value

    def shift_date(self):
        """
        Function to shift date by the offset period
        """
        if not self._offset:
            self._shifted_date = self._original
        else:
            self._shifted_date = self._original + timedelta(days=self._offset)

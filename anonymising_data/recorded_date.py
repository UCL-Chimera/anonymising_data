from datetime import timedelta
from anonymising_data.helpers import create_date, has_expected_date_format


class RecordedDate:
    """
    Class to shift the date and time by prescribed amount
    """
    def __init__(self, original):
        if not has_expected_date_format(original):
            raise ValueError
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
        self._original = create_date(value)

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
        self._shifted_date = create_date(value)

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
        if value not an integer set to 0
        """
        self._offset = value if isinstance(value, int) else 0

    def shift_date(self):
        """
        Function to shift date by the offset period
        """
        self._shifted_date = self._original + timedelta(days=self._offset)

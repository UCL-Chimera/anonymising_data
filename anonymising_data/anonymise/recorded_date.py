from datetime import timedelta
from anonymising_data.utils.helpers \
    import create_date, has_expected_date_format, determine_date_format


class RecordedDate:
    """
    Class to shift the date and time by prescribed amount.
    """

    def __init__(self, original):
        if not has_expected_date_format(original):
            raise ValueError
        self._original_str = original

        self.original = original
        self.offset = 0
        self.shifted_date = original
        self._date_format = determine_date_format(self._original_str)

    @property
    def original_str(self):
        """
        Function to retrieve the original date string.
        :return: _original_str
        """
        return self._original_str

    @property
    def original(self):
        """
        Function to retrieve the original date.
        :return: _original_date
        """
        return self._original

    @original.setter
    def original(self, value):
        """
        Function to set the original date.
        """
        self._original = create_date(value)

    @property
    def shifted_date(self):
        """
        Function to retrieve the shifted date.
        :return: _shifted_date
        """
        return self._shifted_date

    @shifted_date.setter
    def shifted_date(self, value):
        """
        Function to set the shifted date.
        """
        self._shifted_date = create_date(value)

    @property
    def offset(self):
        """
        Function to retrieve the offset period.
        :return: _offset
        """
        return self._offset

    @offset.setter
    def offset(self, value):
        """
        Function to set the offset period in days.
        if value not an integer set to 0.
        """
        self._offset = value if isinstance(value, int) else 0

    def get_shifted_date_str(self):
        """
        Function to set the shifted date.
        """
        month_str = f'{self._shifted_date.month}' \
            if self._shifted_date.month > 9 else f'0{self._shifted_date.month}'
        day_str = f'{self._shifted_date.day}' \
            if self._shifted_date.day > 9 else f'0{self._shifted_date.day}'
        if self._date_format == 0:
            return f'{self._shifted_date.year}/{month_str}/{day_str}'
        elif self._date_format == 1:
            return f'{day_str}/{month_str}/{self._shifted_date.year}'
        elif self._date_format == 2:
            return f'{self._shifted_date.year}-{month_str}-{day_str}'
        elif self._date_format == 3:
            return f'{day_str}-{month_str}-{self._shifted_date.year}'

    def shift_date(self):
        """
        Function to shift date by the offset period.
        """
        self._shifted_date = self._original + timedelta(days=self._offset)

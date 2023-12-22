from pathlib import Path

from anonymising_data.anonymise.age import Age
from anonymising_data.anonymise.recorded_date import RecordedDate


class Data:
    """
    Class to read omop data and do final data shifting.
    """

    def __init__(self, config, sources):
        self._omop_data_file = config.omop_data_file
        self._final_data_file = config.final_data_file
        self._offset = config.date_offset
        self._testing = config.testing
        self._concepts = sources
        self._headers = config.headers
        self.date_cols = config.date_fields
        self.age_cols = config.age_fields

    # FOR USE IN TESTING
    def set_date_fields(self, date_columns):
        self.date_cols = date_columns

    def set_age_fields(self, age_columns):
        self.age_cols = age_columns

    @property
    def omop_data_file(self):
        """
        Function to return filename of omop data file.
        :return:
        """
        return self._omop_data_file

    @property
    def final_data_file(self):
        """
        Function to return filename of final data file.
        :return:
        """
        return self._final_data_file

    def create_final_output(self):
        """
        Function to create final data file.
        :return:
        """
        with open(self._omop_data_file, 'r') as f:
            lines = f.readlines()
        f.close()
        num_lines = len(lines)

        # MAKE output dir if necessary

        Path(self._final_data_file).parent.mkdir(parents=True, exist_ok=True)

        with open(self._final_data_file, 'w') as out:
            with open(self._omop_data_file, 'r') as f:
                # write out first line
                out.write(f.readline())
                for i in range(1, num_lines):
                    line = f.readline()
                    newline = self.adjust_line(line)
                    out.write(newline)

    def adjust_line(self, line):
        """
        Function to adjust the line with anonymised data.
        :param line: Line with original data.
        :return: The line with anonymised data.
        """
        parts = line.split(',')
        # we assume the number of parts equals the number of headers
        # num_parts = len(parts)
        # deal with concepts
        parts[1] = self._concepts[parts[1]]

        # deal with dates
        for column in self.date_cols:
            parts[column] = self.adjust_date_time(parts[column])

        for column in self.age_cols:
            parts[column] = self.find_age(parts[column])

        # rejoin parts
        return ','.join(parts)

    def adjust_date_time(self, line):
        """
        Function to shift times in data.
        :param line: A string representing a date/time.
        :return: A string with the date shifted but the time left as is.
        """
        if not line or line == 'NULL' or line == 'None' or line.startswith(' unspec'):
            return line
        if line.startswith('"'):
            this_date = line[1:11]
            this_time = line[12:len(line) - 1]
        else:
            this_date = line[0:10]
            this_time = line[10:]
        new_date = RecordedDate(this_date)
        new_date.offset = self._offset
        new_date.shift_date()
        return f'{new_date.get_shifted_date_str()}{this_time}'

    def find_age(self, dob):
        """
        A function to return the age based on DOB.
        :param dob: A date object
        :return: An integer representing the age as a string.
        """
        age = Age(dob)
        return f'{age.anon_age}'

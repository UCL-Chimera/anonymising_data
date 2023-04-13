from pathlib import Path

from anonymising_data.anonymise.recorded_date import RecordedDate


class Data:
    """
    Class to read omop data and do final data shifting.
    """
    def __init__(self, config):
        self._omop_data_file = config.omop_data_file
        self._final_data_file = config.final_data_file
        self._offset = 365
        self._testing = config.testing

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
        # columns are
        # measurement_type,person_id,visit,measurement_datetime,
        # value_as_number,units,value_as_string,age,gender,ethnicity
        if self._testing:
            parts[2] = self.adjust_date_time(parts[2])
        else:
            parts[3] = self.adjust_date_time(parts[3])
        return ','.join(parts)

    def adjust_date_time(self, line):
        """
        Function to shift times in data.
        :param line: A string representing a date/time.
        :return: A string with the date shifted but the time left as is.
        """
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

import csv
from pathlib import Path
import re

from anonymising_data.anonymise.age import Age
from anonymising_data.anonymise.recorded_date import RecordedDate


class Data:
    """
    Class to read omop data and do final data shifting.
    """

    def __init__(self, config):
        self._omop_data_file = config._omop_data_file
        self._final_demographic_data = config._final_demographic_data
        self._offset = config.date_offset
        self._testing = config.testing
        self._headers = config.headers_demographic
        self._headers_reading = config.headers_reading
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

    def _create_demographic_output(self):
        """
        Function to retrieve the headers and data for demographic output
        :return: the headers and rows for demographic data
        """
        # TODO: anonymise for dob to age

        new_header = []

        for row in self.lines:
            for h in self._headers_reading:
                elements = [element.strip() for element in row.split(",")]
                if len(elements) > 2 and len(elements) <= 5:
                    prefix = re.sub(r"[^a-zA-Z]", "", elements[0])
                    new_header.append(f"{prefix}_{h}")

        headers = self._headers + new_header
        data_dict = {}
        i = 0
        for row in self.lines:
            elements = [element.strip() for element in row.split(",")[1:]]
            # print(len(elements))
            if len(elements) < 5:
                data_dict[i] = elements
                i += 1

        new_row = []
        values = []

        # Iterate through headers
        for i, field in enumerate(headers):
            if i < len(
                data_dict
            ):  # Check if the index is within the bounds of data_dict
                # Extract values for the current header
                current_values = data_dict[i]

                # If there are multiple values, assign them to the corresponding headers
                while current_values:
                    value = current_values.pop(0)  # Get the first value
                    new_row.append(value)  # Append it to the new row

                    # If there are more headers, add empty strings for the missing values
                    if len(new_row) < i + 1:
                        new_row.extend([""] * (i + 1 - len(new_row)))
            else:
                # If data_dict doesn't have enough elements, add empty strings for the missing headers
                new_row.extend([""] * (i + 1 - len(new_row)))

        # Ensure new_row has the same length as headers
        new_row.extend([""] * (len(headers) - len(new_row)))

        return headers, new_row

    def create_final_output(self):
        """
        Function to create final data file.
        :return:
        """
        with open(self._omop_data_file, "r") as f:
            self.lines = f.readlines()
        f.close()

        # # MAKE output dir if necessary

        Path(self._final_demographic_data).parent.mkdir(parents=True, exist_ok=True)

        with open(self._final_demographic_data, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            headers, new_row = self._create_demographic_output()
            writer.writerow(headers)
            writer.writerow(new_row)

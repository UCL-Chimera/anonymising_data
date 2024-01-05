import csv
from pathlib import Path
import re
import os
from typing import Optional


from anonymising_data.anonymise.age import Age
from anonymising_data.utils.height_weight_helpers import HeightWeightNormalizer


class Data:
    """
    Class to read omop data and do final data shifting.
    """

    def __init__(self, config):
        self._xml_file = config._database
        self._omop_data_file = config.omop_data_file
        self._final_demographic_data = config.final_demographic_data
        self._final_cpet_data = config.final_cpet_data
        self._testing = config.testing
        self._headers = config.headers_demographic
        self._headers_reading = config.headers_reading

    @property
    def omop_data_file(self):
        """
        Function to return filename of omop data file.
        :return:
        """
        return self._omop_data_file

    @property
    def final_cpet_data(self):
        """
        Function to return filename of final data file.
        :return:
        """
        return self._final_cpet_data

    @property
    def final_demographic_data(self):
        """
        Function to return filename of final data file.
        :return:
        """
        return self._final_demographic_data

    def _create_new_header(self, csv_lines):
        """
        Function to create the headers for demographic output
        :return: the headers for demographic data
        """
        new_header = []
        for row in csv_lines:
            for h in self._headers_reading:
                elements = [element.strip() for element in row.split(",")]
                if len(elements) > 2 and len(elements) <= 5:
                    prefix = re.sub(r"[^a-zA-Z'/%2-:]", "", elements[0])
                    new_header.append(f"{prefix}_{h}")

        headers = self._headers + new_header
        return headers

    def _get_demographic_data(self, csv_lines):
        """
        Function to retrieve the headers and data for demographic output
        :return: the headers and rows for demographic data
        """

        data_dict = {}
        i = 0
        for row in csv_lines:
            keys = [key.strip() for key in row.split(",")]
            elements = [element.strip() for element in row.split(",")[1:]]
            if keys[0].lower().startswith("height") or keys[
                0
            ].lower().startswith("weight"):
                normalizer = HeightWeightNormalizer(elements)
                elements = normalizer.normalize_height_weight()

            if len(elements) < 5:
                data_dict[i] = elements
                i += 1

        for i in range(len(data_dict)):
            if i == 2:
                try:
                    data_dict[i] = [str(self.find_age(data_dict[i][0]))]
                except (IndexError, ValueError):
                    pass

        return data_dict

    def _get_demographic_output(self, csv_lines):
        """
        Function to retrieve the headers and data for demographic output
        :return: the headers and rows for demographic data
        """
        headers = self._create_new_header(csv_lines)

        data_dict = self._get_demographic_data(csv_lines)
        new_row = []
        for i, field in enumerate(headers):
            if i < len(data_dict):
                current_values = data_dict[i]
                while current_values:
                    value = current_values.pop(0)
                    new_row.append(value)

                    if len(new_row) < i + 1:
                        new_row.extend([""] * (i + 1 - len(new_row)))
            else:
                new_row.extend([""] * (i + 1 - len(new_row)))

        new_row.extend([""] * (len(headers) - len(new_row)))

        return headers, new_row

    def _get_person_id(self, csv_lines):
        for row in csv_lines:
            key, value = row.strip().split(",")
            lowercase_key = key.lower()
            if lowercase_key == "id" or lowercase_key == "id.-no.":
                self.person_id = value
                break

        self.person_id_found = False

        self.file_exists = (
            os.path.isfile(self._final_demographic_data)
            and os.path.getsize(self._final_demographic_data) > 0
        )

        if self.file_exists:
            with open(self._final_demographic_data, "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if (
                        self.person_id in row[0]
                    ):  # Check if the person_id is in the file
                        self.person_id_found = True

    def _create_demographic_output(self, csv_lines):
        self._get_person_id(csv_lines)

        with open(self._final_demographic_data, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            headers, new_row = self._get_demographic_output(csv_lines)

            if not self.file_exists:
                writer.writerow(headers)
            if not self.person_id_found:
                writer.writerow(new_row)
            else:
                with open(self._final_demographic_data, "r+") as file:
                    lines = file.readlines()
                    file.seek(0)
                    for line in lines:
                        if line.split(",")[0] in self.person_id:
                            file.write(",".join(new_row) + "\n")
                        else:
                            file.write(line)
                    file.truncate()

    def create_final_output(
        self, final_cpet_data, csv_lines: Optional[list] = None
    ):
        """
        Function to create final data file.
        :return:
        """
        xml_files = self._xml_file.glob("*.xml")
        for xml_file in xml_files:
            xml_filename = os.path.basename(xml_file)
            xml_filename, _ = os.path.splitext(xml_filename)
            new_filename = str(self._omop_data_file).replace(
                "x", str(xml_filename)
            )
            omop_csv_file = Path(new_filename)
            if not csv_lines:
                with open(omop_csv_file, "r") as f:
                    csv_lines = f.readlines()
                f.close()

            self._create_demographic_output(csv_lines)

            new_final_cpet_file = final_cpet_data.with_name(
                final_cpet_data.name.replace("x", str(self.person_id))
            )
            Path(new_final_cpet_file).parent.mkdir(parents=True, exist_ok=True)
            with open(new_final_cpet_file, "w") as out:
                for row in csv_lines:
                    elements = [element.strip() for element in row.split(",")]
                    if len(elements) > 6:
                        line_to_write = ",".join(elements) + "\n"
                        out.write(line_to_write)
            print(f"Time series data written to {new_final_cpet_file}")

    def find_age(self, dob):
        """
        A function to return the age based on DOB.
        :param dob: A date object
        :return: An integer representing the age as a string.
        """
        age = Age(dob)
        return f"{age.anon_age}"

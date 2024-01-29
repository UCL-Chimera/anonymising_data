import csv
from pathlib import Path
import re
import os
from typing import Optional

from anonymising_data.anonymise.age import Age
from anonymising_data.utils.height_weight_helpers import HeightWeightNormalizer
from anonymising_data.linking.get_person_id import Link
from anonymising_data.utils.check_filename import extract_and_check_format


class Data:
    """
    Class to read omop data and do final data shifting.
    """

    def __init__(self, config):
        self.config = config
        self._xml_file = config._xml_data
        self._mapping = config._mapping
        self._omop_data_file = config.omop_data_file
        self._final_demographic_data = config.final_demographic_data
        self._final_cpet_data = config.final_cpet_data
        self._testing = config.testing
        self._headers = config.headers_demographic
        self._headers_reading = config.headers_reading

    @property
    def xml_file(self):
        """
        Function to return file path of xml data.
        :return:
        """
        return self._xml_file

    @property
    def mapping(self):
        """
        Function to return csv file of mapping data.
        :return:
        """
        return self._mapping

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
                    prefix = re.sub(r"[^a-zA-Z'/%2-:()]", "", elements[0])
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

    def _get_demographic_output(
        self, csv_lines, person_id: Optional[str] = None
    ):
        """
        Function to retrieve the headers and data for demographic output
        :return: the headers and rows for demographic data
        """
        headers = self._create_new_header(csv_lines)
        data_dict = self._get_demographic_data(csv_lines)
        new_row = []
        for i, field in enumerate(headers):
            if i == 0:
                if not person_id:
                    value = self.person_id
                else:
                    value = person_id
                new_row.append(value)

            elif i < len(data_dict):
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

    def _check_person_id(
        self, demographic_output, person_id: Optional[str] = None
    ):
        """
        Function to retrieve the headers and data for demographic output
        :param demographic_output: The demographic output file.
        :param person_id: The person ID. Optional defaults to None.
        """
        if not person_id:
            person_id = self.person_id
        self.person_id_found = False

        self.file_exists = (
            os.path.isfile(demographic_output)
            and os.path.getsize(demographic_output) > 0
        )

        if self.file_exists:
            with open(demographic_output, "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if (
                        person_id == row[0]
                    ):  # Check if the person_id is in the file
                        self.person_id_found = True

    def _get_person_id(self, csv_lines):
        """
        Function to retrieve the headers and data for demographic output
        :param csv_lines: The contains from the csv.
        :return: The person ID
        """
        for row in csv_lines:
            key, value = row.strip().split(",")
            lowercase_key = key.lower()
            if lowercase_key == "id" or lowercase_key == "id.-no.":
                cpet_id = value
                break

        with open(self._mapping, "r") as f:
            for row in f:
                key, value = row.strip().split(",")
                if cpet_id == key:
                    mrn = value
                    break
                else:
                    mrn = cpet_id

        link = Link(self.config)
        person_id = link.get_person_id(mrn)

        return str(person_id)

    def _create_demographic_output(
        self, csv_lines, demographic_output: Optional[str] = None
    ):
        """
        Function to create and write demographic output.
        :param csv_lines: The contains from the csv.
        :param demographic_output: The demographic output file.
                                    Optional defaults to None.
        """
        self.person_id = self._get_person_id(csv_lines)

        if not demographic_output:
            demographic_output = self._final_demographic_data
            self._check_person_id(demographic_output)
        else:
            self._check_person_id(demographic_output)

        with open(demographic_output, "a", newline="") as csvfile:
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
                        if line.split(",")[0] == self.person_id:
                            file.write(",".join(new_row) + "\n")
                        else:
                            file.write(line)
                    file.truncate()

        return self.person_id

    def _create_time_series_output(self, csv_lines, new_final_cpet_file):
        """
        Function to create and write time_series output.
        :param csv_lines: The contains from the csv.
        :param new_final_cpet_file: The time_series output file.
        :return: The time_series output file.
        """
        with open(new_final_cpet_file, "w") as out:
            for row in csv_lines:
                elements = [element.strip() for element in row.split(",")]
                if len(elements) > 6:
                    line_to_write = ",".join(elements) + "\n"
                    out.write(line_to_write)
        print(f"Time series data written to {new_final_cpet_file}")
        return new_final_cpet_file

    def create_final_output(
        self, final_cpet_data, csv_lines: Optional[list] = None
    ):
        """
        Function to create final data file.
        :param final_cpet_file: The time_series output file.
        :param csv_lines: The contains from the csv. Optional defaults to None.
        """
        xml_filepaths = self._xml_file.glob("*.xml")
        xml_filepaths = list(xml_filepaths)

        person_id_list = []

        for xml_filepath in xml_filepaths:
            xml_filename = os.path.basename(xml_filepath)
            xml_filename, _ = os.path.splitext(xml_filename)
            xml_filename = extract_and_check_format(xml_filename)
            new_filename = str(self._omop_data_file).replace(
                "x", str(xml_filename)
            )

            omop_csv_file = Path(new_filename)
            if not csv_lines:
                with open(omop_csv_file, "r") as f:
                    csv_lines = f.readlines()
                f.close()

            person_id_list.append(self._create_demographic_output(csv_lines))

            new_final_cpet_file = final_cpet_data.with_name(
                final_cpet_data.name.replace("x", str(self.person_id))
            )
            Path(new_final_cpet_file).parent.mkdir(parents=True, exist_ok=True)
            self._create_time_series_output(csv_lines, new_final_cpet_file)

            csv_lines = None

        person_id_csvfile = Path(__file__).parent.parent.joinpath(
            "tests/output/person_id_list.csv"
        )
        with open(person_id_csvfile, "w") as f:
            for id_list in person_id_list:
                f.write(id_list + "\n")
        f.close

        return person_id_list

    def find_age(self, dob):
        """
        A function to return the age based on DOB.
        :param dob: A date object
        :return: An integer representing the age as a string.
        """
        age = Age(dob, self._testing)
        return f"{age.anon_age}"

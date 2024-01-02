import csv
from pathlib import Path
import re
import os


from anonymising_data.anonymise.age import Age


class Data:
    """
    Class to read omop data and do final data shifting.
    """

    def __init__(self, config):
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


    def _create_demographic_output(self):
        """
        Function to retrieve the headers and data for demographic output
        :return: the headers and rows for demographic data
        """
        new_header = []

        # getting the person_id
        for row in self.lines:
            key, value = row.strip().split(",")
            if key == "id" or key == "id.-no.":
                self.person_id = value
                break
        
        # getting the height and weight
        # for row in self.lines:
        #     if len(row) > 1:
        #         print(row["height  (m)"])
        #     # key, value = row.strip().split(",")
        #     # if key == "height":
        #     #     # print(value)
        #     #     break

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
            keys = [key.strip() for key in row.split(",")]
            elements = [element.strip() for element in row.split(",")[1:]]
            if keys[0].lower().startswith("height") or keys[0].lower().startswith("weight"):
                print(elements)
                elements = self.normalize_height_weight(elements)
                print(elements)

            if len(elements) < 5:
                
                data_dict[i] = elements
                i += 1

        for i in range(len(data_dict)):
            if i == 2:
                try:
                    data_dict[i] = [str(self.find_age(data_dict[i][0]))]
                except (IndexError, ValueError):
                    pass

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

    def create_final_output(self):
        """
        Function to create final data file.
        :return:
        """
        with open(self._omop_data_file, "r") as f:
            self.lines = f.readlines()
        f.close()

        # # MAKE output dir if necessary

        Path(self._final_demographic_data).parent.mkdir(
            parents=True, exist_ok=True
        )
        file_exists = (
            os.path.exists(self._final_demographic_data)
            and os.path.getsize(self._final_demographic_data) > 0
        )

        with open(self._final_demographic_data, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            headers, new_row = self._create_demographic_output()

            # If the file is empty or doesn't exist, write headers
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(new_row)

        new_final_cpet_file = self._final_cpet_data.with_name(
            self._final_cpet_data.name.replace("x", str(self.person_id))
        )
        Path(new_final_cpet_file).parent.mkdir(parents=True, exist_ok=True)
        with open(new_final_cpet_file, "w") as out:
            for row in self.lines:
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

    def normalize_height_weight(self, element):
        new_element = None
        element = element[0]
        # Process height
        if "cm" in element or "kg" in element:
            try:
                new_element = float(element.replace("cm", "").replace("kg", "").strip())
            except ValueError:
                pass
        else:
            try:
                new_element = float(element)
            except ValueError:
                pass

        return [str(new_element)]
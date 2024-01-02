from pathlib import Path

import yaml


class Cpet_Config:
    """
    Class to assign config variables.
    """

    def __init__(self, testing=False):
        if testing:
            self.filename = Path(__file__).parent.parent.joinpath(
                "tests", "resources", "cpet_config.yml"
            )
        else:
            self.filename = Path(__file__).parent.parent.parent.joinpath(
                "config.yml"
            )
        self._testing = testing
        self._database = ""
        self._omop_data_file = ""
        self._final_cpet_data = ""
        self._final_demographic_data = ""
        self.headers = []

    @property
    def database(self):
        """
        Function to return filename of database.
        :return:
        """
        return self._database

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
        Function to return the schema.
        :return: schema
        """
        return self._final_demographic_data

    @property
    def testing(self):
        """
        Function to return the value of testing variable.
        :return: testing
        """
        return self._testing

    def read_yaml(self):
        """
        Function to read config and populate variables.
        :return:
        """
        with open(self.filename, "r") as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        f.close()

        self._database = Path(__file__).parent.parent.joinpath(
            cfg["files"]["input"]["concept_mapping"]["filename"]
        )

        self._final_demographic_data = Path(__file__).parent.parent.joinpath(
            cfg["files"]["output"]["demographic_data"]
        )
        self._final_cpet_data = Path(__file__).parent.parent.joinpath(
            cfg["files"]["output"]["time_series_data"]
        )
        self._omop_data_file = Path(__file__).parent.parent.joinpath(
            cfg["files"]["output"]["omop_data"]
        )
        self.headers_exclude = cfg["files"]["input"]["concept_mapping"][
            "headers_exclude"
        ]
        self.headers_demographic = cfg["files"]["output"][
            "headers_demographic"
        ]
        self.headers_reading = cfg["files"]["output"]["headers_reading"]

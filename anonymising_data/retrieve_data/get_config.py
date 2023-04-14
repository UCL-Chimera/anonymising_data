from pathlib import Path

import yaml


class Config:
    """
    Class to assign config variables.
    """

    def __init__(self, testing=False):
        if testing:
            self.filename = Path(__file__).parent.\
                parent.joinpath('tests', 'resources', 'test_config.yml')
        else:
            self.filename = Path(__file__).parent.\
                parent.parent.joinpath('config.yml')

        self._testing = testing
        self._concept_file = ''
        self._query_file = ''
        self._database = ''
        self._output_query_file = ''
        self._omop_data_file = ''
        self._final_data_file = ''
        self._schema = ''
        self._date_offset = None

    @property
    def concept_file(self):
        """
        Function to return filename of concept file.
        :return:
        """
        return self._concept_file

    @property
    def query_file(self):
        """
        Function to return filename of query file.
        :return:
        """
        return self._query_file

    @property
    def database(self):
        """
        Function to return filename of database.
        :return:
        """
        return self._database

    @property
    def output_query_file(self):
        """
        Function to return filename of output query file.
        :return:
        """
        return self._output_query_file

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

    @property
    def schema(self):
        """
        Function to return the schema.
        :return: schema
        """
        return self._schema

    @property
    def date_offset(self):
        """
        Function to return the offset_date.
        :return: date_offset
        """
        return self._date_offset

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
        with open(self.filename, 'r') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
        self._schema = cfg['database']['schema']
        self._date_offset = cfg['anonymisation']['date_offset']
        self._concept_file = Path(__file__).parent.parent.\
            joinpath(cfg['files']['input']['concept_mapping'])
        self._query_file = Path(__file__).parent.parent.\
            joinpath(cfg['files']['input']['db_query'])
        self._database = Path(__file__).parent.parent.\
            joinpath(cfg['database']['path'])
        self._output_query_file = Path(__file__).parent.parent. \
            joinpath(cfg['files']['output']['query'])
        self._final_data_file = Path(__file__).parent.parent. \
            joinpath(cfg['files']['output']['final_data'])
        self._omop_data_file = Path(__file__).parent.parent. \
            joinpath(cfg['files']['output']['omop_data'])

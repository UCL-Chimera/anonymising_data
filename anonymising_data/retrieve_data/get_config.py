import os

import yaml


class Config:
    """
    Class to assign config variables
    """

    def __init__(self):
        self.filename = os.getcwd() + '..' + os.sep + '..' + os.sep + 'config.yml'
        self._year = None
        self._concept_file = ''
        self._query_file = ''

    @property
    def year(self):
        """
        Funcion to return the year
        :return: year
        """
        return self._year

    @property
    def concept_file(self):
        """
        Funcion to return filename of concept file
        :return:
        """
        return self._concept_file

    @property
    def query_file(self):
        """
        Funcion to return filename of query file
        :return:
        """
        return self._query_file

    def read_yaml(self):
        """
        Function to read config and populate variables
        :return:
        """
        with open(self.filename, 'r') as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        self._year = cfg['year']
        self._concept_file = cfg['files']['concept_mapping']
        self._query_file = cfg['files']['db_query']

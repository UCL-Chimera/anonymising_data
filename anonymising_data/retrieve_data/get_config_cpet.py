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
            self.filename = Path(__file__).parent.parent.parent.joinpath("config.yml")

        self._testing = testing
        self._concept_file = ""
        self._query_file = ""
        self._database = ""
        self._output_query_file = ""
        self._omop_data_file = ""
        self._final_data_file = ""
        self._schema = ""
        self._date_offset = None
        self.headers = []
        self.date_fields = []
        self.age_fields = []
        self._username = ""
        self._password = ""
        self._sqlserver = True
        self._driver = ""
        self._server = ""
        self._dbname = ""
        self._port = ""
        self.concepts = {}

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

    @property
    def username(self):
        """
        Function to return username for access to the database.
        :return:
        """
        return self._username

    @property
    def password(self):
        """
        Function to return password for access to the database.
        :return: _password
        """
        return self._password

    @property
    def sqlserver(self):
        """
        Function to return whether this database is an SQL (true) or a PostgreSQL (false).
        :return: _sqlserver
        """
        return self._sqlserver

    @property
    def driver(self):
        """
        Function to return driver for access to the database.
        :return: _driver
        """
        return self._driver

    @property
    def server(self):
        """
        Function to return server for access to the database.
        :return: _server
        """
        return self._server

    @property
    def dbname(self):
        """
        Function to return name for access to the database.
        :return: _dbname
        """
        return self._dbname

    @property
    def port(self):
        """
        Function to return port for access to the database.
        :return: _port
        """
        return self._port

    def read_yaml(self):
        """
        Function to read config and populate variables.
        :return:
        """
        with open(self.filename, "r") as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        f.close()

        # self._schema = cfg['database']['schema']
        # self._password = cfg['database']['password']
        # self._username = cfg['database']['username']
        # self._sqlserver = True if cfg['database']['sqlserver'] else False
        # self._database = Path(__file__).parent.parent.\
        #     joinpath(cfg['database']['path'])
        # self._driver = cfg['database']['driver']
        # self._server = cfg['database']['server']
        # self._dbname = cfg['database']['dbname']
        # self._port = cfg['database']['port']

        self._database = Path(__file__).parent.parent.joinpath(cfg["database"]["path"])

        self._date_offset = cfg["anonymisation"]["date_offset"]
        self.date_fields = cfg["anonymisation"]["dates"]
        self.age_fields = cfg["anonymisation"]["age"]

        # self._concept_file = Path(__file__).parent.parent.\
        #     joinpath(cfg['files']['input']['concept_mapping']['filename'])
        # self._query_file = Path(__file__).parent.parent.\
        #     joinpath(cfg['files']['input']['db_query'])

        # self._output_query_file = Path(__file__).parent.parent. \
        #     joinpath(cfg['files']['output']['query'])
        # self._final_data_file = Path(__file__).parent.parent. \
        #     joinpath(cfg['files']['output']['final_data'])
        self._omop_data_file = Path(__file__).parent.parent.joinpath(
            cfg["files"]["output"]["omop_data"]
        )
        self.headers = cfg["files"]["input"]["concept_mapping"]["headers"]

        # self.concepts = {'filename': self._concept_file,
        #                  'concept_index': cfg['files']['input']['concept_mapping']['concept_index'],
        #                  'source_index': cfg['files']['input']['concept_mapping']['source_index']}

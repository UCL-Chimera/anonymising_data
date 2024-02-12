from pathlib import Path
import yaml


class Cpet_Config:
    """
    Class to assign config variables.
    """
    def __init__(self, data_type, testing=False):
        self.data_type = data_type
        if testing:
            if self.data_type == "sql":
                self.filename = Path(__file__).parent.parent.joinpath(
                    "tests", "resources", "test_config.yml"
                )
            elif self.data_type == "cpet":
                self.filename = Path(__file__).parent.parent.joinpath(
                    "tests", "resources", "cpet_config.yml"
                )
        else:
            self.filename = Path(__file__).parent.parent.parent.joinpath("config.yml")
        self._testing = testing
        self._date_offset = None
        self.date_fields = []
        self.age_fields = []
        self._database = ""
        self._omop_data_file = ""
        self._link_query_file = ""
        self._output_link_query_file = ""
        self._schema = ""
        self._sqlserver = True
        self._driver = ""
        self._server = ""
        self._dbname = ""
        self._port = ""
        self._username = ""
        self._password = ""

        if self.data_type == "cpet":
            self._xml_data = ""
            self._mapping = ""
            self._final_cpet_data = ""
            self._final_demographic_data = ""

        elif self.data_type == "sql":
            self.headers = []
            self.concepts = {}
            self._concept_file = ""
            self._query_file = ""
            self._output_query_file = ""
            self._final_data_file = ""

    @property
    def concept_file(self):
        """
        Function to return filename of concept file.
        :return:
        """
        if hasattr(self, "_concept_file"):
            return self._concept_file
        else:
            return None

    @property
    def query_file(self):
        """
        Function to return filename of query file.
        :return:
        """
        return self._query_file

    @property
    def mapping(self):
        """
        Function to return filename of database.
        :return:
        """
        if hasattr(self, "_xml_mapping_data"):
            return self._xml_mapping_data
        else:
            return None

    @property
    def xml_data(self):
        """
        Function to return filename of database.
        :return:
        """
        if hasattr(self, "_xml_data"):
            return self._xml_data
        else:
            return None

    @property
    def final_cpet_data(self):
        """
        Function to return filename of final data file.
        :return:
        """
        if hasattr(self, "_final_cpet_data"):
            return self._final_cpet_data
        else:
            return None

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

    @property
    def database(self):
        """
        Function to return filename of database.
        :return:
        """
        return self._database

    @property
    def link_query_file(self):
        """
        Function to return filename of query file.
        :return:
        """
        return self._link_query_file

    @property
    def output_link_query_file(self):
        """
        Function to return filename of output query file.
        :return:
        """
        return self._output_link_query_file

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

    def _populate_database_variables(self, cfg):
        """
        Helper function to populate database-related variables.
        """
        db_cfg = cfg.get("database", {})
        self._schema = db_cfg.get("schema")
        self._password = db_cfg.get("password")
        self._username = db_cfg.get("username")
        self._sqlserver = bool(db_cfg.get("sqlserver"))
        self._database = self._construct_file_path(db_cfg.get("path"))
        self._driver = db_cfg.get("driver")
        self._server = db_cfg.get("server")
        self._dbname = db_cfg.get("dbname")
        self._port = db_cfg.get("port")

    def _populate_anonymisation_variables(self, cfg):
        """
        Helper function to populate anonymisation-related variables.
        """
        anonymisation_cfg = cfg.get("anonymisation", {})
        self._date_offset = anonymisation_cfg.get("date_offset")
        self.date_fields = anonymisation_cfg.get("dates")
        self.age_fields = anonymisation_cfg.get("age")

    def _populate_files_variables(self, cfg):
        """
        Helper function to populate files-related variables.
        """
        files_cfg = cfg.get("files", {})
        input_files_cfg = files_cfg.get("input", {})
        output_files_cfg = files_cfg.get("output", {})

        self._xml_data = self._construct_file_path(
            input_files_cfg.get("xml_data", {}).get("filename")
        )
        self._mapping = self._construct_file_path(
            input_files_cfg.get("id_mapping", {}).get("filename")
        )
        self._link_query_file = self._construct_file_path(
            input_files_cfg.get("link_query")
        )
        self._final_demographic_data = self._construct_file_path(
            output_files_cfg.get("demographic_data")
        )
        self._final_cpet_data = self._construct_file_path(
            output_files_cfg.get("time_series_data")
        )
        self._omop_data_file = self._construct_file_path(
            output_files_cfg.get("omop_data")
        )
        self._output_link_query_file = self._construct_file_path(
            output_files_cfg.get("link_query")
        )
        self._concept_file = self._construct_file_path(
            input_files_cfg.get("concept_mapping", {}).get("filename")
        )
        self._query_file = self._construct_file_path(input_files_cfg.get("db_query"))
        self._output_query_file = self._construct_file_path(
            output_files_cfg.get("query")
        )
        self._final_data_file = self._construct_file_path(
            output_files_cfg.get("final_data")
        )
        self.headers = output_files_cfg.get("headers")

    def _construct_file_path(self, filename):
        """
        Helper function to construct file path.
        """
        if filename:
            return Path(__file__).parent.parent.joinpath(filename)
        return None

    def _parse_list_variable(self, cfg, file_type, variable_name):
        """
        Helper function to parse a list variable from the YAML configuration.
        """
        if (
            "files" in cfg and file_type in cfg["files"] and variable_name in cfg["files"][file_type]
        ):
            return cfg["files"][file_type][variable_name]
        return None

    def read_yaml(self):
        """
        Function to read config and populate variables.
        :return:
        """
        with open(self.filename, "r") as f:
            cfg = yaml.load(f, Loader=yaml.FullLoader)
        f.close()

        self._populate_database_variables(cfg)
        self._populate_anonymisation_variables(cfg)
        self._populate_files_variables(cfg)

        self.headers_exclude = self._parse_list_variable(
            cfg, "input", "headers_exclude"
        )
        self.headers_demographic = self._parse_list_variable(
            cfg, "output", "headers_demographic"
        )
        self.headers_reading = self._parse_list_variable(
            cfg, "output", "headers_reading"
        )

        if self.data_type == "sql":
            self.concepts = {
                "filename": self._concept_file,
                "concept_index": cfg["files"]["input"]["concept_mapping"][
                    "concept_index"
                ],
                "source_index": cfg["files"]["input"]["concept_mapping"][
                    "source_index"
                ],
            }

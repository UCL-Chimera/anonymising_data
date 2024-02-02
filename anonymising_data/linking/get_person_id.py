from anonymising_data.retrieve_data.create_query import Query
from anonymising_data.retrieve_data.myconnection import MyConnection
from anonymising_data.retrieve_data.mypostgresconnection import (
    MyPostgresConnection,
)


def construct_connection_string(config):
    connection_string = (
        f"DRIVER={config.driver};Server={config.server};Database={config.dbname};"
        f"Port={config.port};UID={config.username};PWD={config.password};"
    )
    return connection_string


class Link:
    """
    Class to retrieve information to allow different sources of data
    to be linked using the mrn to retrieve the OMOP person_id.
    """

    def __init__(self, config):
        self._data = None
        q = Query(config, None, True)
        q.create_query_file()
        self.pg_connection_string = construct_connection_string(config)
        if config.sqlserver:
            self._conn = MyConnection.create_valid_connection(config.database)
        else:
            self._odbcconn = MyPostgresConnection.create_valid_connection(
                config.database, self.pg_connection_string
            )
            self._conn = MyPostgresConnection(self._odbcconn)
        self._query_file = q._output_query
        self._query = None

    def get_query(self):
        """
        Returns the name of the query file.
        :return: The query file.
        """

        fo = open(self._query_file, "r")
        sql = fo.read()
        self._query = sql
        return sql

    def get_person_id(self, mrn):
        """
        Function to run query and get data.
        :return: data from query
        """
        if self._conn is not None:
            sql = self.get_query()
            sql = sql.rstrip()
            data = self._conn.get_data_query(sql, mrn)
            self._data = data
            return data
        else:
            return None

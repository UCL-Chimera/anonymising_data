from anonymising_data.retrieve_data.create_query import Query
from anonymising_data.retrieve_data.myconnection import MyConnection
from anonymising_data.retrieve_data.mypostgresconnection import MyPostgresConnection


class Link:
    """
    Class to retrieve information to allow different sources of data
    to be linked using the mrn to retrieve the OMOP person_id.
    """
    def __init__(self, config):
        self._data = None
        q = Query(config, None, True)
        q.create_query_file()
        if config.sqlserver:
            self._conn = MyConnection.create_valid_connection(config.database)
        else:
            self._odbcconn = MyPostgresConnection.create_valid_connection(config.database, self.pg_connection_string)
            self._conn = MyPostgresConnection(config.database, self._odbcconn)   
        self._query_file = config.link_query_file
        self._query = None

    @property
    def query(self):
        """
        Returns the name of the query file.

        :return: The query file.
        """
        return self._query

    def get_query(self):
        """
        Get the sql for the query from txt file.
        :return: sql content of file
        """
        fo = open(self._query_file, 'r')
        sql = fo.read()
        self._query = sql
        return sql

    def get_person_id(self, mrn):
        """
        Function to run query and get data.
        :return: data from query
        """
        if self._conn is not None:
            sql = self._query if self._query is not None else self.get_query()
            data = self._conn.get_data_query(sql, mrn)
            self._data = data
            return data
        else:
            return None

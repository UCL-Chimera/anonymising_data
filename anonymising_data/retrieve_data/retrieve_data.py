from anonymising_data.retrieve_data.myconnection import MyConnection
from anonymising_data.retrieve_data.mypostgresconnection import MyPostgresConnection


class RetrieveData:
    """
    Class to retrieve data.
    """

    def __init__(self, config):
        self._query_file = config.output_query_file
        self._testing = config.testing
        if config.sqlserver:
            self._conn = MyConnection.create_valid_connection(config.database)
        else:
            self._odbcconn = MyPostgresConnection.create_valid_connection(config.database)
            self._conn = MyPostgresConnection(config.database, self._odbcconn)
        self._output_file = config.omop_data_file
        self._query = None
        self._data = None

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

    def get_data(self):
        """
        Function to run query and get data.
        :return: data from query
        """
        if self._conn is not None:
            sql = self._query if self._query is not None else self.get_query()
            data = self._conn.get_data_query(sql)
            self._data = data
            return data
        else:
            return None

    def write_data(self):
        """
        A function to output the data retrieved from querying the database.
        If the data has not been read and stored
         this function will call the get_data function.
        """
        dt = self._data if self._data is not None else self.get_data()
        if dt is not None:
            self._conn.close_connection()
            fo = open(self._output_file, 'w')
            if self._testing:
                fo.write('measurement_type,measurement_source,person_id,'
                         'measurement_datetime,'
                         'value_as_number,units,value_as_string,age,gender,'
                         'ethnicity\n')
            else:
                fo.write('measurement_type,measurement_source, person_id,'
                         'visit,measurement_datetime,'
                         'value_as_number,units,value_as_string,age,gender,'
                         'ethnicity\n')
            for row in dt:
                for col in row:
                    fo.write(f'{col},')
                fo.write('\n')
            fo.close()
        else:
            print('A connection to database failed.')

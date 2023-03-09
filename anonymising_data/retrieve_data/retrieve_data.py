from os import error
from pathlib import Path

from anonymising_data.retrieve_data.myconnection import MyConnection


class RetrieveData:
    """
    Class to retrieve data
    """
    def __init__(self, config):
        self.db = config.database
        self.query_file = config.output_query_file
        self.is_mock = config.testing
        self.conn = self.get_connection(config)
        self.output = config.omop_data_file

    def get_connection(self, config):
        """
        Get a connection to the database
        :param: config - config object
        :return: connection to db or exits if the database does not exist
        """
        if self.db is None:
            error('could not find {self.db} database')
            exit(2)
        else:
            return MyConnection(config)

    def get_query(self):
        """
        Get the sql for the query from txt file
        :return: sql content of file
        """
        fo = open(self.query_file, 'r')
        sql = fo.read()
        return sql

    def get_data(self):
        """
            Function to run query and get data`
        :return: data from query
        """
        sql = self.get_query()
        return self.conn.get_data_query(sql)

    def write_data(self):
        dt = self.get_data()
        fo = open(self.output, 'w')
        fo.write('measurement_type,person_id,measurement_datetime,'
                 'value_as_number,units,value_as_string,age,gender,ethnicity\n')
        for row in dt:
            for col in row:
                fo.write(f'{col},')
            fo.write('\n')


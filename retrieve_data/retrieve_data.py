from os import error
from pathlib import Path
from myconnection.myconnection import MyConnection


class RetrieveData:
    """
    Class to retrieve data
    """
    def __init__(self, db, query_file, is_mock=True):
        self.db = db
        self.query_file = query_file
        self.is_mock = is_mock
        self.conn = self.get_connection()

    def get_connection(self):
        """
        Get a connection to the database
        :return: connection to db or exits if the database does not exist
        """
        db_path = self.get_path_for_database()
        if db_path is None:
            error('could not find {self.db} database')
            exit(2)
        else:
            return MyConnection(db_path)

    def get_query(self, testing=False):
        """
        Get the sql for the query from txt file
        :param testing boolean to indicate we are running tests
        :return: sql content of file
        """
        this_dir = Path(__file__).parent.resolve()
        if testing:
            q_file = Path.joinpath(this_dir, '..', 'tests','resources', f'{self.query_file}')
        else:
            q_file = Path.joinpath(this_dir, 'queries', f'{self.query_file}')
        fo = open(q_file, 'r')
        sql = fo.read()
        return sql

    def get_data(self, testing=False):
        """
        Function to run query and get data
        :param testing boolean to indicate we are running tests
        :return: data from query
        """
        sql = self.get_query(testing)
        return self.conn.get_data_query(sql)

    def get_path_for_database(self):
        """
        Get the full path to database eg ./mock-database/mock-{dbn}.sqlite
        :param dbn: name of database
        :return: full path to database
        """
        if self.is_mock:
            this_dir = Path(__file__).parent.resolve()
            db = Path.joinpath(this_dir, '..', 'mock-database', f'mock-{self.db}.sqlite')
            return db
        else:
            # needs customising for whatever we are using
            return None


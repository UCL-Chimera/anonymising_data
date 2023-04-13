import sqlite3


class MyConnection:
    """
    Connection to a database.
    """
    def __init__(self, config):
        self.db_file = config.database
        self.conn = self.create_connection()
        self.cur = MyCursor(self.conn)

    @classmethod
    def create_valid_connection(cls, db_file):
        """
        Function to create a valid connection.
        This allows for error trapping when creating the connection
        and facilitates descriptive error messages.
        :param db_file: Path to the database for which the connection should be made.
        :return: An object MyConnection if a valid connection is made, None otherwise.
        """
        if db_file == '':
            return None
        try:
            conn = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            print(e)
        return conn

    def close_connection(self):
        """
        Close the database connection.
        :param conn: the db connection
        """
        self.conn.close()

    def get_data_query(self, sql):
        """
        Function to run an sql query to fetch data.
        :param sql: sql to execute
        :return: data
       """
        return self.cur.get_data_query(sql)

    def execute_query(self, sql):
        """
        Function to execute a query that returns nothing
        :param sql: sql to execute
        """
        self.cur.execute_query(sql)
        self.conn.commit()


class MyCursor:
    """
    Class for the connection cursor.
    """
    def __init__(self, conn):
        self.cur = conn.cursor()

    def get_data_query(self, sql):
        """
        Function to run an sql query to fetch data.
        :param sql: sql to execute
        :return: data
        """
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

    def execute_query(self, sql):
        """
        Function to execute a query that returns nothing
        :param sql: sql to execute
        """
        self.cur.execute(sql)

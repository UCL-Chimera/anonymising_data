import sqlite3


class MyConnection:
    """
    connection to a database
    """
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.create_connection()
        self.cur = MyCursor(self.conn)

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by the db_file
        :return: Connection object or None
        """
        try:
            self.conn = sqlite3.connect(self.db_file)
        except sqlite3.Error as e:
            print(e)
        return self.conn

    def close_connection(self):
        """
        Close the database connection
        :param conn: the db connection
        """
        self.conn.close()

    def get_data_query(self, sql):
        """
        Function to run an sql query to fetch data
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
    class for the connection cursor
    """
    def __init__(self, conn):
        self.cur = conn.cursor()

    def get_data_query(self, sql):
        """
        Function to run an sql query to fetch data
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
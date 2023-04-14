import sqlite3


class MyConnection:
    """
    connection to a database
    """
    def __init__(self, database, conn):
        self.db_file = database
        self.conn = conn
        self.cur = MyCursor(self.conn)

    @classmethod
    def create_valid_connection(cls, db_file):
        if db_file == '':
            return None
        try:
            conn = sqlite3.connect(db_file)
        except (sqlite3.Error, TypeError):
            return None
        else:
            return cls(db_file, conn)

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
        return self.cur.get_data(sql)


class MyCursor:
    """
    class for the connection cursor
    """
    def __init__(self, conn):
        self.cur = conn.cursor()

    def get_data(self, sql):
        """
        Function to run an sql query to fetch data
        :param sql: sql to execute
        :return: data
        """
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

import sqlite3


class MyConnection:
    """
    Connection to a database.
    """

    def __init__(self, database, conn):
        self.db_file = database
        self.conn = conn
        self.cur = MyCursor(self.conn)

    @classmethod
    def create_valid_connection(cls, db_file):
        """
        Function to create a valid connection.
        This allows for error trapping when creating the connection
        and facilitates descriptive error messages.
        :param db_file: Path to the database for which the
         connection should be made.
        :return: An object MyConnection if a valid connection is made,
         None otherwise.
        """
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
        Close the database connection.
        :param conn: the db connection
        """
        self.conn.close()

    def get_data_query(self, sql, mrn=None):
        """
        Function to run an sql query to fetch data.
        :param sql: sql to execute
        :param mrn
        :return: data
        """
        return self.cur.get_data(sql, mrn)


class MyCursor:
    """
    Class for the connection cursor.
    """

    def __init__(self, conn):
        self.cur = conn.cursor()

    def get_data(self, sql, mrn=None):
        """
        Function to run an sql query to fetch data.
        :param sql: sql to execute
        :return: data
        """
        if mrn:
            value = (mrn,)
            self.cur.execute(sql, value)
            data = self.cur.fetchall()
            if len(data) > 0:
                return data[0][0]
            else:
                return None
        else:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            return data

import psycopg2
import pyodbc

class MyPostgresConnection:
    """
    Connection to a database.
    """

    def __init__(self, database, conn):
        self.db_file = database
        self.conn = conn
        self.cur = MyPGCursor(self.conn)

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
            conn = pyodbc.connect("DRIVER={PostgreSQL Unicode};Server=uclvlddpragae06;"
                                  "Database=omop_reservoir;Port=15432;UID=skeating;"
                                  "PWD=CherryBlossom_2022;")
        except (Exception, pyodbc.Error) as error:
            print(error)
            return None
        except (Exception, pyodbc.Warning) as error:
            print(error)
            return None
        else:
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
        return self.cur.get_data(sql)


class MyPGCursor:
    """
    Class for the connection cursor.
    """

    def __init__(self, conn):
        self.cur = conn.cursor()

    def get_data(self, sql):
        """
        Function to run an sql query to fetch data.
        :param sql: sql to execute
        :return: data
        """
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data

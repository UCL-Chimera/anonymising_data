import sqlite3
from pathlib import Path


def get_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn


def close_connection(conn):
    """
    Close the database connection
    :param conn: the db connection
    """
    conn.close()


def get_path_for_mock_database(dbn):
    """
    Get the full path to database eg ./mock-database/mock-{dbn}.sqlite
    :param dbn: name of database
    :return: full path to database
    """
    this_dir = Path(__file__).parent.resolve()
    db = Path.joinpath(this_dir, '..', 'mock-database', f'mock-{dbn}.sqlite')
    return db


def main():
    db = get_path_for_mock_database()
    conn = get_connection(db)


if __name__ == '__main__':
    main()

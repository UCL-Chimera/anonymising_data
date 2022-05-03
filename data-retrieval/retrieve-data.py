import sqlite3
from pathlib import Path


def get_query(query_file):
    """
    Get the sql for the query from txt file
    :param query_file: name of file to get
    :return: sql content of file
    """
    this_dir = Path(__file__).parent.resolve()
    q_file = Path.joinpath(this_dir, 'queries', f'{query_file}')
    fo = open(q_file, 'r')
    sql = fo.read()
    return sql


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


def get_data(query_file, conn):
    """

    :param query_file:
    :param conn:
    :return:
    """
    sql = get_query(query_file)
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    return data


def main():
    db = get_path_for_mock_database('caboodle')
    conn = get_connection(db)
    data = get_data('patientTemp', conn)
    print(data)


if __name__ == '__main__':
    main()

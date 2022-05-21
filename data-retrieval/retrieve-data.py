from pathlib import Path

from myconnection.myconnection import MyConnection


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
    Function to run query and get data
    :param query_file: name of file containing the sql query
    :param conn: connection to database
    :return: data from query
    """
    sql = get_query(query_file)
    return conn.get_data_query(sql)


def main():
    db = get_path_for_mock_database('caboodle')
    conn = MyConnection(db)
    data = get_data('patientTemp', conn)
    print(data)


if __name__ == '__main__':
    main()

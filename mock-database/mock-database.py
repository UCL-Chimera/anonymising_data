import sqlite3
from pathlib import Path


database_names = ['caboodle']
"""
names of test databases to create
"""


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


def get_paths_for_database(dbn):
    """
    Get the full path to database eg ./test-database/test-{dbn}.sqlite
    and the path for the ddl and data files
    :param dbn: name of database
    :return: [full path to database, ddl_dir, data_dir]
    """
    this_dir = Path(__file__).parent.resolve()
    db = Path.joinpath(this_dir, f'test-{dbn}.sqlite')
    ddl = Path.joinpath(this_dir, f'{dbn}_ddl')
    data = Path.joinpath(this_dir, f'{dbn}_data')
    return[db, ddl, data]


def create_table(conn, ddlfile):
    """
    create the table in the ddl file
    :param conn: connection to db
    :param ddlfile: file containing create sql ddl
    """
    cur = conn.cursor()
    sql = Path(ddlfile).read_text()
    cur.execute(sql)
    conn.commit()


def get_table_name(ddlfile):
    """
    gets the database tablename form the sql
    :param ddlfile: ddl file for the table
    :return: the tablename being created
    """
    f = open(ddlfile, 'r')
    line = f.readline()
    parts = line.split(' ')
    tblname = parts[2]
    f.close()
    return tblname


def populate_table(conn, datafile, tablename):
    """
    populate table with datafrom csv
    :param conn: connection to db
    :param datafile: path to datafile
    :param tablename name of table to populate
    """
    cur = conn.cursor()
    fin = open(datafile, 'r')
    lines = fin.readlines()
    fin.close()
    # dont want the header line
    newlines = lines[1:]
    for line in newlines:
        sql = f'INSERT INTO {tablename} VALUES ({line})'
        cur.execute(sql)
        conn.commit()


def get_corresponding_datafile(ddlfile, data):
    """
    gets the csv file with same name as ddl
    :param ddlfile: ddlfile
    :param data: data directory
    :return: path to csv file with same name as ddlfile
    """
    tablename = Path(ddlfile).stem
    return Path.joinpath(data, f'{tablename}.csv')


def create_and_populate_tables(conn, ddl, data):
    """
    Create and populate a table corresponding to each ddl/data file
    :param conn: connection to db
    :param ddl: dir containing ddl files
    :param data: dir containing data files
    """
    for ddlfile in Path.iterdir(ddl):
        create_table(conn, ddlfile)
        datafile = get_corresponding_datafile(ddlfile, data)
        populate_table(conn, datafile, get_table_name(ddlfile))


def remove_existing_databases():
    for dbn in database_names:
        [db, a, b] = get_paths_for_database(dbn)
        Path.unlink(db, missing_ok=True)


def main():
    remove_existing_databases()
    for dbn in database_names:
        [db, ddl, data] = get_paths_for_database(dbn)
        conn = get_connection(db)
        create_and_populate_tables(conn, ddl, data)
        close_connection(conn)


if __name__ == '__main__':
    main()

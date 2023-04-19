from pathlib import Path

from anonymising_data.retrieve_data.myconnection import MyConnection


def test_create_connection(config):
    """
    Function to test the create_valid_connection function
    :param config: Configuration class from Pytest fixtures
    """
    conn = MyConnection.create_valid_connection(config._database)
    assert (conn is not None)
    assert (conn.cur is not None)
    assert (conn.db_file == Path(__file__).parent.parent.
            joinpath('tests/resources/mock-database/test_omop_es.sqlite3'))


def test_failed_connection(config):
    """

    :param config:
    :return:
    """
    config._database = None
    conn = MyConnection.create_valid_connection(config._database)
    assert (conn is None)


def test_failed_connection1(config):
    config._database = ''
    conn = MyConnection.create_valid_connection(config._database)
    assert (conn is None)


from pathlib import Path

from anonymising_data.retrieve_data.get_config import Config
from anonymising_data.retrieve_data.myconnection import MyConnection

import pytest


@pytest.fixture(scope="session")
def config():
    cfg = Config(testing=True)
    cfg.read_yaml()
    return cfg


def test_create_connection(config):
    conn = MyConnection.create_valid_connection(config._database)
    assert (conn is not None)
    assert (conn.cur is not None)
    assert (conn.db_file == Path(__file__).parent.parent.
            joinpath('tests/resources/mock-database/test_omop_es.sqlite3'))


def test_failed_connection(config):
    config._database = None
    conn = MyConnection.create_valid_connection(config._database)
    assert (conn is None)


def test_failed_connection1(config):
    config._database = ''
    conn = MyConnection.create_valid_connection(config._database)
    assert (conn is None)


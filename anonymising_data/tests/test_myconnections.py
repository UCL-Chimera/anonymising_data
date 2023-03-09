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
    conn = MyConnection(config)
    assert (conn is not None)
    assert (conn.cur is not None)
    assert (conn.db_file == Path(__file__).parent.parent.
            joinpath('tests/resources/mock-database/test_omop_es.sqlite3'))
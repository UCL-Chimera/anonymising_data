from anonymising_data.retrieve_data.get_config import Config
from anonymising_data.myconnection.myconnection import MyConnection, MyCursor

import pytest


@pytest.fixture(scope="session")
def config():
    cfg = Config(testing=True)
    cfg.read_yaml()
    return cfg


def test_create_connection(config):
    conn = MyConnection(config)
    assert (conn is not None)


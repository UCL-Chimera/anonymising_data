from anonymising_data.retrieve_data.get_config import Config
from anonymising_data.retrieve_data.get_concepts import Concepts
from anonymising_data.retrieve_data.create_query import Query

import pytest


@pytest.fixture(scope="session")
def config():
    cfg = Config(testing=True)
    cfg.read_yaml()
    return cfg


@pytest.fixture(scope="session")
def concept_file(config):
    return config.concept_file


@pytest.fixture(scope="session")
def year(config):
    return config.year


@pytest.fixture(scope="session")
def query_file(config):
    return config.query_file


@pytest.fixture(scope="session")
def concepts(concept_file):
    con = Concepts(concept_file)
    con.populate_concepts()
    return con.concepts


def test_create_query(config, concepts):
    # cfg = Config(testing=True)
    # con = Concepts(cfg.concept_file)
    # con.populate_concepts()
    #
    q = Query(config, concepts)
    assert (q is not None)

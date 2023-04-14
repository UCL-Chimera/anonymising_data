import pytest

from anonymising_data.retrieve_data.get_concepts import Concepts
from anonymising_data.retrieve_data.get_config import Config


@pytest.fixture(scope="session")
def config():
    cfg = Config(testing=True)
    cfg.read_yaml()
    return cfg


@pytest.fixture(scope="session")
def concept_file(config):
    return config.concept_file


@pytest.fixture(scope="session")
def concepts(concept_file):
    con = Concepts(concept_file)
    con.populate_concepts()
    return con.concepts

import pytest

from anonymising_data.retrieve_data.get_concepts import Concepts
from anonymising_data.retrieve_data.get_config import Config


@pytest.fixture(scope="session")
def config():
    """
    Create an instance of the config class and read the appropriate yaml file.

    :return: An instance of the config class fully populated.
    """
    cfg = Config(testing=True)
    cfg.read_yaml()
    return cfg


@pytest.fixture(scope="session")
def concept_file(config):
    """
    Return the concept file from the configuration class.

    :param config: The configuration class
    :return: The concept file attribute of the configuration class
    """
    return config.concept_file


@pytest.fixture(scope="session")
def concepts(concept_file):
    """
    Create an instance of concepts class and populate it.

    :param concept_file: The name of the file containing the concepts
    :return: The concepts attribute of the concepts class
    """
    con = Concepts(concept_file)
    con.populate_concepts()
    return con.concepts


@pytest.fixture(scope="session")
def sources(concept_file):
    """
    Create an instance of concepts class and populate it.

    :param concept_file: The name of the file containing the concepts
    :return: The concepts attribute of the concepts class
    """
    con = Concepts(concept_file)
    con.populate_concepts()
    return con.source

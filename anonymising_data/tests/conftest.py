import pytest

from anonymising_data.retrieve_data.get_concepts import Concepts
from anonymising_data.retrieve_data.get_config import Config
from anonymising_data.retrieve_data.get_config_cpet import Cpet_Config


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
def concepts(config):
    """
    Create an instance of concepts class and populate it.

    :param concept_file: The name of the file containing the concepts
    :return: The concepts attribute of the concepts class
    """
    con = Concepts(config)
    con.populate_concepts()
    return con.concepts


@pytest.fixture(scope="session")
def sources(config):
    """
    Create an instance of concepts class and populate it.

    :param concept_file: The name of the file containing the concepts
    :return: The concepts attribute of the concepts class
    """
    con = Concepts(config)
    con.populate_concepts()
    return con.source


@pytest.fixture(scope="session")
def xml_config():
    """
    Create an instance of the cpet config class and read the appropriate yaml file.

    :return: An instance of the xml config class fully populated.
    """
    xml_cfg = Cpet_Config(testing=True)
    xml_cfg.read_yaml()
    return xml_cfg

from pathlib import Path

from anonymising_data.retrieve_data.get_concepts import Concepts

import pytest


10
@pytest.mark.parametrize("line, concept_id, source", [
    ('400, SNOMED, 432, Body temperature, S1, Measurement', '432', 'S1'),
    ('12 - Jul, LOINC, 543, Oxygen[Partial pressure], S2, Measurement', '543', 'S2'),
])
def test_get_concept(config, line, concept_id, source):
    """
    Function to test reading the concept ID
    :param line: The line read from the results of the query file.
    :param concept_id: The expected concept ID
    """
    con = Concepts(config)
    assert (con.get_concept_id_and_source(line) == [concept_id, source])


def test_get_concepts(config):
    """
    Function to test the populate_concepts function
    :param config: Concepts from Pytest fixtures
    :return:
    """
    con = Concepts(config)
    con.populate_concepts()
    assert (con.concepts == ['1', '23', '5872'])


def test_get_sources(config):
    """
    Function to test the populate_concepts function
    returns dictionary of ids and sources
    :param config: Concepts from Pytest fixtures
    :return:
    """
    con = Concepts(config)
    con.populate_concepts()
    assert (con.source == {'1': 'TEMPERATURE',
                           '23': 'AQURE TEMPERATURE CORRECTED OXYGEN',
                           '5872': 'Source'})


def test_create_concepts_cpet(config_cpet):
    """
    Function to test creation of a concepts object.
    :param config: Concepts from Pytest fixtures
    """
    con = Concepts(config_cpet)
    assert (con is not None)
    assert (con._filename == Path(__file__).parent.parent.
            joinpath('tests/resources/test_concept_codes_cpet.csv'))
    

def test_get_concepts_cpet(config_cpet):
    """
    Function to test the populate_concepts function
    :param config: Concepts from Pytest fixtures
    :return:
    """
    con = Concepts(config_cpet)
    con.populate_concepts()
    assert (con.concepts == ['35775967', '4239021', '32817'])

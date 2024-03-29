import filecmp
from pathlib import Path

from anonymising_data.retrieve_data.create_query import Query


def test_create_query(config, concepts):
    """
    Function to test that a query object is created.
    :param config: Configuration class from Pytest fixtures
    :param concepts: Concepts from Pytest fixtures
    """
    q = Query(config, concepts)
    assert (q is not None)


def test_write_query(config, concepts):
    """
    Function to test the create_query_file by comparing with an example given.
    :param config: Configuration class from Pytest fixtures
    :param concepts: Concepts from Pytest fixtures
    """
    q = Query(config, concepts)
    q.create_query_file()
    newfile = Path(__file__).parent.parent.\
        joinpath('tests/output/get_data.sql')
    testfile = Path(__file__).parent.parent.\
        joinpath('tests/resources/test_query_expected.sql')
    assert (filecmp.cmp(newfile, testfile, shallow=False))


def test_adjust_line(config, concepts):
    """
    A function to test the adjust_line function.
    :param config: Configuration class from Pytest fixtures
    :param concepts: Concepts from Pytest fixtures
    """
    q = Query(config, concepts)
    assert (q is not None)
    q._con_str = '()'
    line = ':FILL_CONCEPT:'
    newline = q.adjust_line(line)
    assert (newline == '()')
    line = ':FILL_SCHEMA:'
    newline = q.adjust_line(line)
    assert (newline == '')
    q._issql = False
    newline = q.adjust_line(line)
    assert (newline == 'mock_omop_es.')


def test_write_link_query(config, concepts):
    """
    Function to test the create_query_file by comparing with an example given.
    :param config: Configuration class from Pytest fixtures
    :param concepts: Concepts from Pytest fixtures
    """
    q = Query(config, concepts, True)
    q.create_query_file()
    newfile = Path(__file__).parent.parent.\
        joinpath('tests/output/get_link.sql')
    testfile = Path(__file__).parent.parent.\
        joinpath('tests/resources/link_query_expected.sql')
    assert (filecmp.cmp(newfile, testfile, shallow=False))


def test_write_cpet_query(config_cpet, concepts_cpet, person_id_cpet):
    """
    Function to test the create_query_file by comparing with an example given.
    :param config: Configuration class from Pytest fixtures
    :param concepts: Concepts from Pytest fixtures
    """
    q = Query(config_cpet, concepts_cpet, person_id=person_id_cpet)
    q.create_query_file()
    newfile = Path(__file__).parent.parent.\
        joinpath('tests/output/get_data_cpet.sql')
    testfile = Path(__file__).parent.parent.\
        joinpath('tests/resources/cpet_ehr_data/expected_get_measurement.sql')
    assert (filecmp.cmp(newfile, testfile, shallow=False))

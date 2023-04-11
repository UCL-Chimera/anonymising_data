import filecmp
from pathlib import Path

from anonymising_data.retrieve_data.get_config import Config
from anonymising_data.retrieve_data.retrieve_data import RetrieveData

import pytest


@pytest.fixture(scope="session")
def config():
    cfg = Config(testing=True)
    cfg.read_yaml()
    return cfg


def test_create_retrieve_data(config):
    d = RetrieveData(config)
    assert (d is not None)
    assert (d._query_file == Path(__file__).parent.parent.
            joinpath('tests/output/get_data.sql'))
    assert (d._conn is not None)


def test_get_query(config):
    d = RetrieveData(config)
    sql = d.get_query()
    assert (sql == 'SELECT\n    c.concept_name AS measurement_type,\n'
                   '    m.person_id,\n    m.measurement_datetime,\n'
                   '    m.value_as_number,\n'
                   '	m.unit_source_value AS units,\n    (\n'
                   '        SELECT cc.concept_name FROM concept AS cc\n'
                   '        WHERE cc.concept_id = m.value_as_concept_id\n'
                   '            AND cc.concept_name NOT LIKE '
                   '\'No matching concept\'\n'
                   '    ) AS value_as_string,\n'
                   '    p.date_of_birth AS age,\n'
                   '    p.gender_source_value AS gender,\n'
                   '    p.race_source_value AS ethnicity\n'
                   'FROM measurement AS m\n\n'
                   'INNER JOIN person AS p\n'
                   '    ON m.person_id = p.person_id\n\n'
                   'INNER JOIN concept AS c\n'
                   '    ON c.concept_id = m.measurement_concept_id\n\n'
                   'WHERE\n\n'
                   '    m.measurement_concept_id IN (1, 23, 5872)\n\n'
                   'ORDER BY m.person_id\n')


def test_get_data(config):
    d = RetrieveData(config)
    dt = d.get_data()
    assert (len(dt) == 3)


def test_z_write_data(config):
    config.read_yaml()
    d = RetrieveData(config)
    d.write_data()
    newfile = Path(__file__).parent.parent.\
        joinpath('tests/output/omop_data.csv')
    testfile = Path(__file__).parent.parent.\
        joinpath('tests/resources/test_expected_omop.csv')
    assert (filecmp.cmp(newfile, testfile, shallow=False))
    fo = open(d._output_file, 'r')
    line1 = fo.readline()
    parts = line1.split(',')
    assert (len(parts) == 9)


def test_write_data_non_test(config):
    d = RetrieveData(config)
    dt = d.get_data()
    d._testing = False
    d.write_data()
    fo = open(d._output_file, 'r')
    line1 = fo.readline()
    parts = line1.split(',')
    assert (len(parts) == 10)


def test_get_data_fail(config):
    config._testing = True
    config.read_yaml()
    config._database = None
    d = RetrieveData(config)
    dt = d.get_data()
    assert (dt is None)


def test_write_data_fail(config):
    config.read_yaml()
    d = RetrieveData(config)
    d._conn = None
    d.write_data()
    assert (d._data is None)

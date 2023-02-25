from pathlib import Path

from anonymising_data.retrieve_data.final_output import Data

import pytest

from anonymising_data.retrieve_data.get_config import Config


@pytest.fixture(scope="session")
def config():
    cfg = Config(testing=True)
    cfg.read_yaml()
    return cfg


def test_create_query(config):
    d = Data(config)
    assert (d is not None)
    assert (d.omop_data_file == Path(__file__).parent.parent.
            joinpath('tests/resources/test_data.csv'))
    assert (d.final_data_file == Path(__file__).parent.parent.
            joinpath('tests/output/final_data.csv'))


@pytest.mark.parametrize("testdate, shifted", [
    ('2000-02-10 03:21', '2001-02-09 03:21'),
    ('1999-02-10 22:16', '2000-02-10 22:16'),
])
def test_shift_date(config, testdate, shifted):
    d = Data(config)
    assert(d.adjust_date_time(testdate) == shifted)


@pytest.mark.parametrize("testdate, shifted", [
    ('0,1,2,2000-02-10 03:21,4,5,6', '0,1,2,2001-02-09 03:21,4,5,6'),
    ('a,b,c,1999-02-10 22:16,d,e,f', 'a,b,c,2000-02-10 22:16,d,e,f'),
])
def test_adjust_line(config, testdate, shifted):
    d = Data(config)
    assert (d.adjust_line(testdate) == shifted)

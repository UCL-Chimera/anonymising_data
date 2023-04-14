# import filecmp
import filecmp
from pathlib import Path

from anonymising_data.retrieve_data.final_output import Data

import pytest

from anonymising_data.retrieve_data.get_config import Config
from anonymising_data.retrieve_data.retrieve_data import RetrieveData


@pytest.fixture(scope="session")
def config():
    cfg = Config(testing=True)
    cfg.read_yaml()
    return cfg


def test_create_data(config):
    d = Data(config)
    assert (d is not None)
    assert (d.omop_data_file == Path(__file__).parent.parent.
            joinpath('tests/output/omop_data.csv'))
    assert (d.final_data_file == Path(__file__).parent.parent.
            joinpath('tests/output/final_data.csv'))


@pytest.mark.parametrize("testdate, shifted", [
    ('2000-02-10 03:21', '2001-02-09 03:21'),
    ('1999-02-10 22:16', '2000-02-10 22:16'),
])
def test_shift_date(config, testdate, shifted):
    d = Data(config)
    assert (d.adjust_date_time(testdate) == shifted)


@pytest.mark.parametrize("testdata, shifted", [
    ('0,1,2000-02-10 03:21,4,5', '0,1,2001-02-09 03:21,4,5'),
    ('a,c,1999-02-10 22:16,d,e', 'a,c,2000-02-10 22:16,d,e'),
])
def test_adjust_line(config, testdata, shifted):
    d = Data(config)
    assert (d.adjust_line(testdata) == shifted)


@pytest.mark.parametrize("testdata, shifted", [
    ('0,1,2000-02-10 03:21,4,5,6,1991-03-10', '0,1,2001-02-09 03:21,4,5,6,32'),
    ('a,c,1999-02-10 22:16,d,e,f,1966-07-05', 'a,c,2000-02-10 22:16,d,e,f,57'),
])
def test_find_age(config, testdata, shifted):
    d = Data(config)
    assert (d.adjust_line(testdata) == shifted)


def test_write_data(config):
    # need correct testing data in our output file
    config.read_yaml()
    rd = RetrieveData(config)
    rd.write_data()
    # now do test
    d = Data(config)
    d.create_final_output()
    newfile = Path(__file__).parent.parent.\
        joinpath('tests/output/final_data.csv')
    testfile = Path(__file__).parent.parent.\
        joinpath('tests/resources/test_expected_data.csv')
    assert (filecmp.cmp(newfile, testfile, shallow=False))


@pytest.mark.parametrize("testdata, shifted", [
    ('0,1,1,2000-02-10 03:21,4,5,6,1991-03-10', '0,1,1,2001-02-09 03:21,4,5,6,32'),
    ('a,c,c,1999-02-10 22:16,d,e,f,1966-07-05', 'a,c,c,2000-02-10 22:16,d,e,f,57'),
])
def test_adjust_line_not_test(config, testdata, shifted):
    d = Data(config)
    d._testing = False
    assert (d.adjust_line(testdata) == shifted)

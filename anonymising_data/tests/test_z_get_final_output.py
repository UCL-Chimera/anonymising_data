# import filecmp
import filecmp
from pathlib import Path

from anonymising_data.retrieve_data.final_output import Data

import pytest

from anonymising_data.retrieve_data.retrieve_data import RetrieveData


def test_create_data(config, sources):
    """
    Function to test Data class is created.

    :param config: Configuration class from Pytest fixtures
    """
    d = Data(config, sources)
    assert (d is not None)
    assert (d.omop_data_file == Path(__file__).parent.parent.
            joinpath('tests/output/omop_data.csv'))
    assert (d.final_data_file == Path(__file__).parent.parent.
            joinpath('tests/output/final_data.csv'))
    assert (d._concepts == {'1': 'TEMPERATURE',
                            '23': 'AQURE TEMPERATURE CORRECTED OXYGEN',
                            '5872': 'Source'})


@pytest.mark.parametrize("testdate, shifted", [
    ('2000-02-10 03:21', '2001-02-09 03:21'),
    ('1999-02-10 22:16', '2000-02-10 22:16'),
])
def test_shift_date(config, sources, testdate, shifted):
    """
    Test dates are shifted as expected.

    :param config:
    :param testdate:
    :param shifted:
    :return:
    """
    d = Data(config, sources)
    assert (d.adjust_date_time(testdate) == shifted)


@pytest.mark.parametrize("testdata, shifted", [
    ('0,1,1,2000-02-10 03:21,4,5', '0,TEMPERATURE,1,2001-02-09 03:21,4,5'),
    ('a,1,c,1999-02-10 22:16,d,e', 'a,TEMPERATURE,c,2000-02-10 22:16,d,e'),
])
def test_adjust_line(config, sources, testdata, shifted):
    """

    :param config:
    :param testdata:
    :param shifted:
    :return:
    """
    d = Data(config, sources)
    d.set_date_fields([3])
    d.set_age_fields([])
    assert (d.adjust_line(testdata) == shifted)


@pytest.mark.parametrize("testdata, shifted", [
    ('0,1,1,2000-02-10 03:21,4,5,6,1991:03:10 00:00:00',
     '0,TEMPERATURE,1,2001-02-09 03:21,4,5,6,33'),
    ('a,1,c,1999-02-10 22:16,d,e,f,1966-07-05',
     'a,TEMPERATURE,c,2000-02-10 22:16,d,e,f,58'),
])
def test_find_age(config, sources, testdata, shifted):
    """

    :param config: Configuration class from Pytest fixtures
    :param testdata:
    :param shifted:
    :return:
    """
    d = Data(config, sources)
    d.set_date_fields([3])
    d.set_age_fields([7])
    assert (d.adjust_line(testdata) == shifted)


def test_write_data(config, sources):
    """

    :param config: Configuration class from Pytest fixtures
    :return:
    """
    # need correct testing data in our output file
    config.read_yaml()
    rd = RetrieveData(config)
    rd.write_data()
    # now do test
    d = Data(config, sources)
    d.create_final_output()
    newfile = Path(__file__).parent.parent.\
        joinpath('tests/output/final_data.csv')
    testfile = Path(__file__).parent.parent.\
        joinpath('tests/resources/test_expected_data.csv')
    assert (filecmp.cmp(newfile, testfile, shallow=False))


@pytest.mark.parametrize("testdata, shifted", [
    ('0,1,1,2000-02-10 03:21,4,5,6,1991:03:10 00:00:00',
     '0,TEMPERATURE,1,2001-02-09 03:21,4,5,6,33'),
    ('a,1,c,1999-02-10 22:16,d,e,f,1966-07-05',
     'a,TEMPERATURE,c,2000-02-10 22:16,d,e,f,58'),
])
def test_adjust_line_not_test(config, sources, testdata, shifted):
    """

    :param config: Configuration class from Pytest fixtures
    :param testdata:
    :param shifted:
    :return:
    """
    d = Data(config, sources)
    d.set_date_fields([3])
    d.set_age_fields([7])
    assert (d.adjust_line(testdata) == shifted)


def test_write_data_cpet(config_cpet):
    """

    :param config: Configuration class from Pytest fixtures
    :return:
    """
    # need correct testing data in our output file
    config_cpet.read_yaml()
    rd = RetrieveData(config_cpet)
    rd.write_data()
    # now do test
    d = Data(config_cpet)
    d.create_final_output()
    newfile = Path(__file__).parent.parent.\
        joinpath('tests/output/final_data_cpet_measurement.csv')
    testfile = Path(__file__).parent.parent.\
        joinpath('tests/resources/cpet_ehr_data/expected_measurement_data.csv')
    assert (filecmp.cmp(newfile, testfile, shallow=False))
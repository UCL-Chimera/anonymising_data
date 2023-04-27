import datetime

import pytest
from anonymising_data.anonymise.recorded_date import RecordedDate
from anonymising_data.utils.helpers import create_date


def test_create_recorded_date():
    """
    Test that the recorded date object is correctly created.

    """
    dd = datetime.datetime(2023, 11, 10, 0, 0)
    d = RecordedDate('10/11/2023')
    assert (d is not None)
    assert (d.original_str == '10/11/2023')
    assert (d.original == dd)
    assert (d.shifted_date == dd)
    assert (d.offset == 0)


@pytest.mark.parametrize("testdate, offset, shifted", [
    ('2000-02-10', 367, '2001-02-11'),
    ('1999-02-10', 367, '2000-02-12'),
    ('2000-03-10', 53, '2000-05-02'),
    ('2000-03-10', -10, '2000-02-29'),
    ('2000-03-10', 0, '2000-03-10'),
    ('2000/03/10', -40, '2000/01/30'),
    ('10-07-1966', 730, '09-07-1968'),
    ('01/04/1969', 730, '01/04/1971'),
])
def test_shift_date(testdate, offset, shifted):
    """
    Test to check shift date function works as expected
    :param testdate: original date
    :param offset: days to shift by
    :param shifted: shifted date
    """
    start = RecordedDate(testdate)
    start.offset = offset
    assert start.original == create_date(testdate)
    assert start.offset == offset
    start.shift_date()
    assert start.shifted_date == create_date(shifted)
    assert start.get_shifted_date_str() == shifted


@pytest.mark.parametrize("testdate", [
    '1066',
    '2000-03-x4',
    '1999-03/23',
    '2000-3-10',
    '10-2-67',
])
def test_bad_date_format(testdate):
    """
    Test that incorrect date formats do not populate class
    :param testdate: date string
    """
    try:
        start = RecordedDate(testdate)
    except ValueError:
        start = None
    assert (not start)


@pytest.mark.parametrize("testdate, offset", [
    ('2000-02-10', 36.7),
    ('1999-02-10', '36%'),
    ('2000-03-10', 5 / 3),
    ('2000-03-10', -1.0),
])
def test_bad_offset_value(testdate, offset):
    """
    Test to check incorrect offsets get caught
    :param testdate: original date
    :param offset: days to shift by
    """
    start = RecordedDate(testdate)
    assert start
    start.offset = offset

    assert start.original == create_date(testdate)
    assert start.offset == 0
    start.shift_date()
    assert start.shifted_date == create_date(testdate)

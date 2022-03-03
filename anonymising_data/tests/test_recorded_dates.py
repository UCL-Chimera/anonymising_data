import pytest
from datetime import datetime
from anonymising_data.recorded_date import RecordedDate


@pytest.mark.parametrize("testdate, offset, shifted", [
    ('2000-02-10', 367, '2001-02-11'),
    ('1999-02-10', 367, '2000-02-12'),
    ('2000-03-10', 53, '2000-05-02'),
    ('2000-03-10', -10, '2000-02-29'),
    ('2000-03-10', 0, '2000-03-10'),
])
def test_shift_date(testdate, offset, shifted):
    """
    Test to check shift date function works as expected
    :param testdate: original date
    :param offset: days to shift by
    :param shifted: shifted date
    :return:    """
    start = RecordedDate(testdate)
    start.offset = offset
    assert start.original == datetime.strptime(testdate, '%Y-%m-%d')
    assert start.offset == offset
    start.shift_date()
    assert start.shifted_date == datetime.strptime(shifted, '%Y-%m-%d')


@pytest.mark.parametrize("testdate", [
    '1066',
    '10-02-2000',
    '2000-03-x4',
    '1999-03/23',
    '1999/02/10',
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
    ('2000-03-10', 5/3),
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

    assert start.original == datetime.strptime(testdate, '%Y-%m-%d')
    assert start.offset == 0
    start.shift_date()
    assert start.shifted_date == datetime.strptime(testdate, '%Y-%m-%d')

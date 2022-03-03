import pytest
from datetime import datetime
from anonymising_data.recorded_date import RecordedDate


@pytest.mark.parametrize("testdate, offset, shifted", [
    ('2000-02-10', 367, '2001-02-11'),
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
    start.shift_date()
    assert(start.shifted_date == datetime.strptime(shifted, '%Y-%m-%d'))

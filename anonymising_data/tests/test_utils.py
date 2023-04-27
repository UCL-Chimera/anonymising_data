from anonymising_data.utils.helpers import determine_date_format,\
    has_expected_date_format, rreplace

import pytest


@pytest.mark.parametrize("date_str, correct_format", [
    ('2000-2-10', False),
    ('1999-02-10', True),
    ('2023/08/10', True),
    ('13-09-4321', True),
    ('21/12/3090', True),
    ('2000-02/10', False),
    ('2000:02:10', True),
])
def test_has_expected_format(date_str, correct_format):
    """
    Test date string has correct format.

    :param date_str: date as string
    :param correct_format: True if format correct, False otherwise
    """
    assert (has_expected_date_format(date_str) is correct_format)


@pytest.mark.parametrize("date_str, correct_format", [
    ('1999-02-10', 2),
    ('2023/08/10', 0),
    ('13-09-4321', 3),
    ('21/12/3090', 1),
    ('2009:09:09', 4)
])
def test_get_date_format(date_str, correct_format):
    """
    Test the format of date string is correct.

    :param date_str: date as string
    :param correct_format: 0-4 from format enum (range)
    """
    assert (determine_date_format(date_str) == correct_format)


@pytest.mark.parametrize("original, old, new, occurrences, produced", [
    ('test1', 't', 'W', 1, 'tesW1'),
    ('test1', 't', 'W', 2, 'WesW1'),
    ('test1', 't', 'W', 3, 'WesW1'),
    ('test1', 'a', 'W', 1, 'test1'),
    ('this is a test it is', 'is', 'REP', 1, 'this is a test it REP'),
    ('this is a test it is', 'is', 'REP', 3, 'thREP REP a test it REP'),
])
def test_rreplace(original, old, new, occurrences, produced):
    """
    Function to test rreplace function
    :param original: original string
    :param old: string to be replaced
    :param new: string replacement
    :param occurrences: no of occurences to replace
    :param produced: result string
    """
    assert (rreplace(original, old, new, occurrences) == produced)

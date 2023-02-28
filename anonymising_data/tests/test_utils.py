from anonymising_data.utils.helpers import determine_date_format,\
    has_expected_date_format

import pytest


@pytest.mark.parametrize("date_str, correct_format", [
    ('2000-2-10', False),
    ('1999-02-10', True),
    ('2023/08/10', True),
    ('13-09-4321', True),
    ('21/12/3090', True)
])
def test_has_expected_format(date_str, correct_format):
    assert (has_expected_date_format(date_str) is correct_format)


@pytest.mark.parametrize("date_str, correct_format", [
    ('1999-02-10', 2),
    ('2023/08/10', 0),
    ('13-09-4321', 3),
    ('21/12/3090', 1)
])
def test_get_date_format(date_str, correct_format):
    assert (determine_date_format(date_str) == correct_format)

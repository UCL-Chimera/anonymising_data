from anonymising_data.utils.helpers import has_expected_date_format

import pytest


@pytest.mark.parametrize("date_str, correct_format", [
    ('2000-2-10', False),
    ('1999-02-10', True),
    ('2023/08/10', True)
])
def test_has_expected_format(date_str, correct_format):
    assert (has_expected_date_format(date_str) is correct_format)

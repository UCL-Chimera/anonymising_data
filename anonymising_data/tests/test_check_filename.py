import pytest

from anonymising_data.utils.check_filename import extract_and_check_format


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        ("CPET702-JOE-BLOGGS", "CPET702"),
        ("CPX_CPET702_JOE_30012021_1112", "CPET702"),
        ("CPET0818-TONY-JONES", "CPET0818"),
        ("CPET0818_JONES_30122023_0504", "CPET0818"),
    ],
)
def test_extract_and_check_format(input_data, expected_output):
    """
    Test the extract_and_check_format function.

    :param input_data: Input data to the function
    :param expected_output: Expected output after extraction
    """
    result = extract_and_check_format(input_data)
    assert result == expected_output

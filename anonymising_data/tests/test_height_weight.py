import pytest

from anonymising_data.utils.height_weight_helpers import HeightWeightNormalizer


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        (["180cm"], ["180.0"]),
        (["80kg"], ["80.0"]),
        (["1.8"], ["180.0"]),
        (["2"], ["200.0"]),
        (["150"], ["150.0"]),
    ],
)
def test_normalize_height_weight(input_data, expected_output):
    """
    Test the normalize_height_weight function.

    :param input_data: Input data to the function
    :param expected_output: Expected output after normalization
    """
    instance = HeightWeightNormalizer(input_data)
    result = instance.normalize_height_weight()
    assert result == expected_output

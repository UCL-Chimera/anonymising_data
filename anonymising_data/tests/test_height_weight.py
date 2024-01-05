import pytest

from anonymising_data.utils.height_weight_helpers import HeightWeightNormalizer


@pytest.mark.parametrize(
    "input_data, expected_output",
    [
        (["180cm"], ["180.0"]),  # Valid height in cm
        (["80kg"], ["80.0"]),  # Valid weight in kg
        (["1.8"], ["180.0"]),  # Height in meters (converted to cm)
        (["2"], ["200.0"]),  # Numeric input less than 3 (assumed meters)
        (["150"], ["150.0"]),  # Numeric input without units
    ],
)
def test_normalize_height_weight(input_data, expected_output):
    """
    Test the normalize_height_weight function.

    :param input_data: Input data to the function
    :param expected_output: Expected output after normalization
    """
    instance = HeightWeightNormalizer(
        input_data
    )  # Replace YourClass with your actual class name
    result = instance.normalize_height_weight()
    assert result == expected_output

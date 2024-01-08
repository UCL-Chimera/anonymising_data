import pytest
import csv
import tempfile
from pathlib import Path

from anonymising_data.retrieve_data.final_output_xml import Data


@pytest.fixture
def instance(xml_config):
    """
    Fixture to create an instance of the Data class with the
    provided XML configuration.
    :param xml_config: Configuration class from Pytest fixtures.
    :return: An instance of the Data class.
    """
    xml_config.read_yaml()
    d = Data(xml_config)
    return d


# def _get_person_id
def test_person_id_found(instance):
    """
    Function to test erson_id existence.
    :param instance: An instance of Data class.
    """
    demographic_data = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/cpet_demographics_report_data.csv"
    )

    instance._check_person_id(demographic_data, "CPET702")
    assert instance.person_id_found is True


def test_person_id_not_found(instance):
    """
    Function to test person_id existence.
    :param instance: An instance of Data class.
    """
    demographic_data = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/cpet_demographics_report_data.csv"
    )

    instance._check_person_id(demographic_data, "02")
    assert instance.person_id_found is False


def test_file_does_not_exist(instance):
    """
    Function to test file existence.
    :param instance: An instance of Data class.
    """
    demographic_data = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/non_exist_file.csv"
    )
    instance._check_person_id(demographic_data, "02")
    assert instance.file_exists is False


@pytest.mark.parametrize(
    "csv_lines, expected_header",
    [
        (
            [
                "t,mm:ss,00:00 - 03:00,10:08,12:16 - 12:46\n",
                "METS,na,0.8,2.7,4.4\n",
                "%HRR,%,100,39,2\n",
            ],
            [
                "person_id",
                "age",
                "gender",
                "height",
                "weight",
                "t_Unit",
                "t_Rest",
                "t_AT",
                "t_V'O2peak",
                "METS_Unit",
                "METS_Rest",
                "METS_AT",
                "METS_V'O2peak",
                "%HRR_Unit",
                "%HRR_Rest",
                "%HRR_AT",
                "%HRR_V'O2peak",
            ],
        ),
    ],
)
def test_new_header(instance, csv_lines, expected_header):
    """
    Function to test new header.
    :param instance: An instance of Data class.
    """
    headers = instance._create_new_header(csv_lines)
    assert headers == expected_header


def test_create_new_header(instance):
    """
    Function to test create header.
    :param instance: An instance of Data class.
    """
    csvfile = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/omop_person_id_01_cpet_data.csv"
    )

    testfile = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/cpet_demographics_report_data.csv"
    )

    with open(testfile, "r") as file:
        reader = csv.reader(file)
        expected_header = next(reader)

    with open(csvfile, "r") as f:
        csv_lines = f.readlines()
    f.close()
    headers = instance._create_new_header(csv_lines)
    assert headers == expected_header


def test_get_demographic_data_empty(instance):
    """
    Function to test get_demographic_data function.
    :param instance: An instance of Data class.
    """
    csv_lines = []
    expected_output = {}
    output = instance._get_demographic_data(csv_lines)

    assert output == expected_output


@pytest.mark.parametrize(
    "csv_lines, expected_output",
    [
        (
            [
                "ID,09\n",
                "Sex,female\n",
                "Date of Birth,1970-01-25T00:00:00.000\n",
                "Height,1.53 \n",
                "Weight,70 kg\n",
                "t,mm:ss,00:00 - 03:00,10:08,12:16 - 12:46\n",
            ],
            {
                0: ["09"],
                1: ["female"],
                2: ["54"],
                3: ["153.0"],
                4: ["70.0"],
                5: ["mm:ss", "00:00 - 03:00", "10:08", "12:16 - 12:46"],
            },
        ),
    ],
)
def test_get_demographic_data(instance, csv_lines, expected_output):
    """
    Function to test get_demographic_data function.
    :param instance: An instance of Data class.
    """
    output = instance._get_demographic_data(csv_lines)
    assert output == expected_output


@pytest.mark.parametrize(
    "csv_lines, expected_rows",
    [
        (
            [
                "ID,09\n",
                "Sex,female\n",
                "Date of Birth,1970-01-25T00:00:00.000\n",
                "Height,1.53 \n",
                "Weight,70 kg\n",
                "t,mm:ss,00:00 - 03:00,10:08,12:16 - 12:46\n",
            ],
            [
                "09",
                "female",
                "54",
                "153.0",
                "70.0",
                "mm:ss",
                "00:00 - 03:00",
                "10:08",
                "12:16 - 12:46",
            ],
        ),
    ],
)
def test_get_demographic_output(instance, csv_lines, expected_rows):
    """
    Function to test function to get demographic output.
    :param instance: An instance of Data class.
    """
    headers, rows = instance._get_demographic_output(csv_lines)
    assert rows == expected_rows
    assert len(headers) == len(expected_rows)


def test_write_demographic_output(instance):
    """
    Function to test function to get demographic output.
    :param instance: An instance of Data class.
    """
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        csvfile = Path(__file__).parent.parent.joinpath(
            "tests/resources/CPet/test-files/expected-files/omop_person_id_01_cpet_data.csv"
        )
        with open(csvfile, "r") as f:
            csv_lines = f.readlines()
        instance._create_demographic_output(csv_lines, temp_file.name)

        csvfile = Path(__file__).parent.parent.joinpath(
            "tests/resources/CPet/test-files/expected-files/omop_person_id_02_cpet_data.csv"
        )
        with open(csvfile, "r") as f:
            csv_lines = f.readlines()
        instance._create_demographic_output(csv_lines, temp_file.name)

    with open(temp_file.name, "r") as f:
        demographic_output = f.readlines()

    testfile = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/cpet_demographics_report_data.csv"
    )
    with open(testfile, "r") as f:
        demographic_expected = f.readlines()

    assert demographic_output == demographic_expected


def test_write_time_series_output(instance):
    """
    Function to test write time series output.
    :param instance: An instance of Data class.
    """
    temp_fd, temp_csv_path = tempfile.mkstemp(suffix=".csv")
    temp_csv = Path(temp_csv_path)

    csvfile = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/omop_person_id_01_cpet_data.csv"
    )
    with open(csvfile, "r") as f:
        csv_lines = f.readlines()

    print(temp_csv)

    time_series_output_path = instance._create_time_series_output(
        csv_lines, temp_csv
    )

    assert time_series_output_path == temp_csv

    with open(time_series_output_path, "r") as f:
        time_series_output = f.readlines()
    f.close()

    print(time_series_output)

    assert time_series_output is not None

    testfile = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/OMOP_person_id_01_time_series_cpet.csv"
    )

    with open(testfile, "r", encoding="utf-8-sig") as f:
        time_series_expected = f.readlines()
    f.close()
    print(time_series_expected)

    assert time_series_expected == time_series_output


def test_write_final_output():
    """
    Function to test write final output.
    :param instance: An instance of Data class.
    """
    final_cpet_data = Path(__file__).parent.parent.joinpath(
        "tests/output/omop_person_id_x_time_series.cpt"
    )
    new_final_cpet_file = final_cpet_data.with_name(
        final_cpet_data.name.replace("x", str("09"))
    )

    assert new_final_cpet_file == Path(__file__).parent.parent.joinpath(
        "tests/output/omop_person_id_09_time_series.cpt"
    )

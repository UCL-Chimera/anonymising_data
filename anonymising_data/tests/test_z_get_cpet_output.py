import pytest
import filecmp
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


def test_person_id_found(instance):
    """
    Function to test erson_id existence.
    :param instance: An instance of Data class.
    """
    instance._final_demographic_data = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/cpet_demographics_report_data.csv"
    )
    instance._get_person_id(["ID,CPET702"])
    assert instance.person_id_found is True


def test_person_id_not_found(instance):
    """
    Function to test person_id existence.
    :param instance: An instance of Data class.
    """
    instance._final_demographic_data = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/cpet_demographics_report_data.csv"
    )
    instance._get_person_id(["ID,01"])
    assert instance.person_id_found is False


def test_file_does_not_exist(instance):
    """
    Function to test file existence.
    :param instance: An instance of Data class.
    """
    instance._final_demographic_data = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/non_exist_file.csv"
    )
    instance._get_person_id(["ID,CPET702"])
    assert instance.file_exists is False


def test_write_demographic_output(instance, xml_config):
    """
    Function to test function to write demographic output.
    :param instance: An instance of Data class.
    :param xml_config: Configuration class from Pytest fixtures.
    """
    csvfile = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/omop_person_id_01_cpet_data.csv"
    )
    with open(csvfile, "r") as f:
        csv_lines = f.readlines()
    f.close()

    headers, rows = instance._get_demographic_output(csv_lines)
    assert len(headers) == 21

    # instance._create_demographic_output(csv_lines)

    # testfile = Path(__file__).parent.parent.joinpath(
    #     "tests/resources/CPet/test-files/expected-files/cpet_demographics_report_data.csv"
    # )
    # assert filecmp.cmp(demographic_file, testfile, shallow=False)
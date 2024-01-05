import os
import filecmp
import pytest
from pathlib import Path
import csv
import tempfile

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


def test_get_demographic_output(instance, xml_config):
    """
    Function to test the retrieval of demographic output using an instance 
    of a class and XML configuration.
    :param instance: An instance of Data class.
    :param xml_config: Configuration class from Pytest fixtures.
    """
    xml_directory = xml_config._database / "test-files"

    xml_files = [
        file for file in os.listdir(xml_directory) if file.endswith(".xml")
    ]

    for xml_file in xml_files:
        xml_filename = os.path.basename(xml_file)
        xml_filename, _ = os.path.splitext(xml_filename)

        newfile = (
            Path(__file__).parent.parent
            / "tests"
            / "output"
            / f"omop_{xml_filename}_cpet_data.csv"
        )

        with open(newfile, "r") as f:
            lines = f.readlines()
        f.close()

        headers, rows = instance._get_demographic_output(lines)
        assert len(headers) == 97


def test_create_new_header(instance, xml_config):
    """
    Function to test new header.
    :param instance: An instance of Data class.
    :param xml_config: Configuration class from Pytest fixtures.
    """
    testfile = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/cpet_demographics_report_data.csv"
    )

    with open(testfile, "r") as file:
        reader = csv.reader(file)
        expected_header = next(reader)

    xml_directory = xml_config._database / "test-files"

    xml_files = [
        file for file in os.listdir(xml_directory) if file.endswith(".xml")
    ]

    for xml_file in xml_files:
        xml_filename = os.path.basename(xml_file)
        xml_filename, _ = os.path.splitext(xml_filename)

        newfile = (
            Path(__file__).parent.parent
            / "tests"
            / "output"
            / f"omop_{xml_filename}_cpet_data.csv"
        )

        with open(newfile, "r") as f:
            lines = f.readlines()
        f.close()

        headers = instance._create_new_header(lines)

        num_elements_to_compare = min(len(expected_header), len(headers))
        assert (
            headers[:num_elements_to_compare]
            == expected_header[:num_elements_to_compare]
        )


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
    xml_directory = xml_config._database / "test-files"
    xml_files = [
        file for file in os.listdir(xml_directory) if file.endswith(".xml")
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        demographic_file = os.path.join(
            temp_dir, "demographic_report_data_new.csv"
        )

        instance._final_demographic_data = demographic_file

        for xml_file in xml_files:
            xml_filename = os.path.basename(xml_file)
            xml_filename, _ = os.path.splitext(xml_filename)

            newfile = (
                Path(__file__).parent.parent
                / "tests"
                / "output"
                / f"omop_{xml_filename}_cpet_data.csv"
            )

            with open(newfile, "r") as f:
                csv_lines = f.readlines()
            f.close()
            instance._create_demographic_output(csv_lines)

        testfile = Path(__file__).parent.parent.joinpath(
            "tests/resources/CPet/test-files/expected-files/cpet_demographics_report_data.csv"
        )

        assert filecmp.cmp(demographic_file, testfile, shallow=False)


def test_z_write_final_data(instance, xml_config):
    """
    Functions to test the function to write final data.
    :param instance: An instance of Data class.
    :param xml_config: Configuration class from Pytest fixtures
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        # Mock XML files
        xml_directory = xml_config._database / "test-files"
        xml_files = [
            file for file in os.listdir(xml_directory) if file.endswith(".xml")
        ]

        for xml_file in xml_files:
            xml_filename = os.path.basename(xml_file)
            xml_filename, _ = os.path.splitext(xml_filename)

            newfile = (
                Path(__file__).parent.parent
                / "tests"
                / "output"
                / f"omop_{xml_filename}_cpet_data.csv"
            )

            with open(newfile, "r") as f:
                csv_lines = f.readlines()

            final_output_file = (
                Path(temp_dir) / f"{xml_filename}_final_output.csv"
            )
            instance.create_final_output(final_output_file, csv_lines)

            assert os.path.exists(final_output_file)

            testfile = (
                Path(__file__).parent.parent
                / "tests"
                / "resources"
                / "CPet"
                / "test-files"
                / "expected-files"
                / f"OMOP_person_id_{xml_filename}_time_series_cpet.csv"
            )

            with open(final_output_file, "r") as f_output, open(
                testfile, "r"
            ) as f_expected:
                output_content = f_output.read()
                expected_content = f_expected.read()

            assert output_content == expected_content

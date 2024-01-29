import pytest
import os
import tempfile
from pathlib import Path

from anonymising_data.retrieve_data.final_output_xml import Data
from anonymising_data.retrieve_data.retrieve_xml import RetrieveXML


@pytest.fixture
def instance(xml_config):
    """
    Fixture to create an instance of the Data class with the
    provided XML configuration.
    :param xml_config: Configuration class from Pytest fixtures.
    :return: An instance of the Data class.
    """
    xml_config.read_yaml()
    d = RetrieveXML(xml_config)
    w = Data(xml_config)
    return d, w


@pytest.fixture
def xml_directory(xml_config):
    """
    Fixture to provide the path to the directory containing sample XML files.
    """
    return xml_config._xml_data


def test_person_id_mapping(instance):
    """
    Functions to test the mapping of person_id from cpet_id.
    :param xml_config: Configuration class from Pytest fixtures
    """
    expected_person_id = ["1", "7341", "6327"]

    cpet_id = [["ID,CPET702\n"], ["ID,CPET0818\n"], ["ID,CPET705\n"]]
    _, final_output = instance
    n = 0

    for i in cpet_id:
        person_id = final_output._get_person_id(i)
        assert expected_person_id[n] == person_id
        n += 1


def test_person_id_list(instance, xml_directory):
    """
    Functions to test the list of person_id.
    :param xml_config: Configuration class from Pytest fixtures
    """
    expected_person_id = ["1", "7341", "6327"]
    retriever, final_output = instance
    xml_files = [
        file for file in os.listdir(xml_directory) if file.endswith(".xml")
    ]
    person_id_list = []

    for xml_file in xml_files:
        file_path = os.path.join(xml_directory, xml_file)
        csv_files = retriever.get_data(file_path)

        with open(csv_files, "r") as output_file:
            output_csv_content = output_file.readlines()
        output_file.close()

        person_id_list.append(
            final_output._create_demographic_output(output_csv_content)
        )

    assert expected_person_id == person_id_list


def preprocess_list(input_list):
    """Convert 'na' and empty cells to a common representation in a list of strings."""
    processed_rows = []
    for row in input_list:
        elements = row.split(",")
        processed_row = [
            cell.strip() if cell.strip() != "" else "na" for cell in elements
        ]
        processed_rows.append(processed_row)
    return processed_rows


def test_write_demographic_output(instance, xml_directory):
    """
    Functions to test the list of person_id.
    :param xml_config: Configuration class from Pytest fixtures
    """
    retriever, final_output = instance
    xml_files = [
        file for file in os.listdir(xml_directory) if file.endswith(".xml")
    ]

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_output = temp_file.name
        for xml_file in xml_files:
            print(xml_file)
            file_path = os.path.join(xml_directory, xml_file)
            csv_files = retriever.get_data(file_path)

            with open(csv_files, "r") as output_file:
                output_csv_content = output_file.readlines()

                final_output._create_demographic_output(
                    output_csv_content, temp_output
                )

        with open(temp_output, "r") as f:
            demographic_output = f.readlines()

        expected_file = Path(__file__).parent.parent.joinpath(
            "tests/resources/CPet/expected-output/cpet_demographics_report_data.csv"
        )
        with open(expected_file, "r") as f:
            demographic_expected = f.readlines()

        assert set(demographic_output) == set(demographic_expected)

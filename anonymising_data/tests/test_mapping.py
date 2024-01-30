import pytest
import os
import tempfile
from pathlib import Path
import pandas as pd

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
    expected_person_id = ["7341", "6327", "1"]
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

    assert set(expected_person_id) == set(person_id_list)


def test_write_demographic_output(instance, xml_directory):
    """
    Functions to test the list of person_id.
    :param xml_config: Configuration class from Pytest fixtures
    """
    retriever, final_output = instance
    file_path = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/expected-input/CPET0818-TONY-JONES.xml"
    )

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_output = temp_file.name
        csv_files = retriever.get_data(file_path)

        with open(csv_files, "r") as output_file:
            output_csv_content = output_file.readlines()

            final_output._create_demographic_output(
                output_csv_content, temp_output
            )
        demographic_output_df = pd.read_csv(temp_output)

        expected_file = Path(__file__).parent.parent.joinpath(
            "tests/resources/CPet/expected-output/cpet_demographics_report_data.csv"
        )
        demographic_expected_df = pd.read_csv(expected_file)

        columns_to_check = ["person_id", "gender", "age", "height", "weight"]

        is_row_in_output_df = (
            (
                demographic_output_df[columns_to_check]
                == demographic_expected_df.iloc[1][columns_to_check]
            )
            .all(axis=1)
            .any()
        )

        assert is_row_in_output_df

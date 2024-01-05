import os
import filecmp
from pathlib import Path
import pytest

from anonymising_data.retrieve_data.retrieve_xml import RetrieveXML


@pytest.fixture
def instance(xml_config):
    """
    Fixture to create an instance of the Data class with the provided XML configuration.
    :param xml_config: Configuration class from Pytest fixtures.
    :return: An instance of the Data class.
    """
    xml_config.read_yaml()
    d = RetrieveXML(xml_config)
    return d


@pytest.fixture
def xml_directory(xml_config):
    """
    Fixture to provide the path to the directory containing sample XML files.
    """
    return xml_config._database / "test-files"


def test_xml_file_existence(instance):
    """
    Function to test the existence of an XML file based on the given configuration.
    :param instance: An instance of Data class.
    """
    assert instance.xml_file.exists()


def test_data_retrieval(xml_config, xml_directory):
    """
    Functions to test the XML data retrieval.
    :param xml_config: Configuration class from Pytest fixtures
    """
    retriever = RetrieveXML(xml_config)

    xml_files = [
        file for file in os.listdir(xml_directory) if file.endswith(".xml")
    ]

    for xml_file in xml_files:
        file_path = os.path.join(xml_directory, xml_file)
        data = retriever.get_data(file_path)
        assert isinstance(data, list)
        assert len(data) > 0


def test_z_write_data(xml_config, xml_directory):
    """
    Functions to test the write_data function.
    :param xml_config: Configuration class from Pytest fixtures
    """
    retriever = RetrieveXML(xml_config)

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

        retriever.write_data()

        testfile = (
            Path(__file__).parent.parent
            / "tests"
            / "resources"
            / "CPet"
            / "test-files"
            / "expected-files"
            / f"omop_{xml_filename}_cpet_data.csv"
        )

        assert filecmp.cmp(newfile, testfile, shallow=False)

        with open(newfile, "r") as generated_file:
            line1 = generated_file.readline()
            parts = line1.split(",")
            assert len(parts) > 1
        with open(newfile, "r") as csvfile:
            csv_content = csvfile.read()
            assert any(
                keyword not in csv_content
                for keyword in retriever.headers_exclude
            )

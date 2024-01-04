import os
import filecmp
from pathlib import Path

from anonymising_data.retrieve_data.retrieve_xml import RetrieveXML


def test_xml_file_existence(xml_config):
    xml_config.read_yaml()
    retriever = RetrieveXML(xml_config)
    assert retriever.xml_file.exists()


def test_data_retrieval(xml_config):
    retriever = RetrieveXML(xml_config)
    xml_directory = xml_config._database

    xml_directory = xml_directory / "test-files"

    xml_files = [file for file in os.listdir(xml_directory) if file.endswith(".xml")]

    for xml_file in xml_files:
        file_path = os.path.join(xml_directory, xml_file)
        data = retriever.get_data(file_path)
        assert len(data) > 0


def test_z_write_data(xml_config, tmp_path):
    """
    Functions to test the write_data function.
    :param config: Configuration class from Pytest fixtures
    """
    retriever = RetrieveXML(xml_config)

    xml_directory = xml_config._database / "test-files"

    # Get a list of XML files in the specified directory
    xml_files = [file for file in os.listdir(xml_directory) if file.endswith(".xml")]

    for xml_file in xml_files:
        xml_filename = os.path.basename(xml_file)
        xml_filename, _ = os.path.splitext(xml_filename)

        newfile = (
            Path(__file__).parent.parent
            / "tests"
            / "output"
            / f"omop_{xml_filename}_cpet_data.csv"
        )

        retriever.write_data(newfile)

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
                keyword not in csv_content for keyword in retriever.headers_exclude
            )

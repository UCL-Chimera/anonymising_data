import os
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
    d = RetrieveXML(xml_config, "xml")
    return d


@pytest.fixture
def xml_directory(xml_config):
    """
    Fixture to provide the path to the directory containing sample XML files.
    """
    return xml_config._xml_data


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
    retriever = RetrieveXML(xml_config, "xml")

    xml_files = [file for file in os.listdir(xml_directory) if file.endswith(".xml")]

    for xml_file in xml_files:
        file_path = os.path.join(xml_directory, xml_file)
        data = retriever.get_xml_data(file_path)
        assert isinstance(data, list)
        assert len(data) > 0


def test_xml_retrieval(xml_config):
    """
    Functions to test the write_data function.
    :param xml_config: Configuration class from Pytest fixtures
    """
    xml_content = """
    <Root xmlns:doc="urn:schemas-microsoft-com:office:spreadsheet">
        <doc:Row>
            <doc:Cell>
                <doc:Data>Cell 1</doc:Data>
            </doc:Cell>
            <doc:Cell>
                <doc:Data>Cell 2</doc:Data>
            </doc:Cell>
        </doc:Row>
        <doc:Row>
            <doc:Cell>
                <doc:Data>Cell 3</doc:Data>
            </doc:Cell>
            <doc:Cell>
                <doc:Data>Cell 4</doc:Data>
            </doc:Cell>
        </doc:Row>
    </Root>
    """
    temp_xml_file = "temp.xml"
    with open(temp_xml_file, "w") as file:
        file.write(xml_content)

    retriever = RetrieveXML(xml_config, "xml")
    data = retriever.get_xml_data(temp_xml_file)
    assert isinstance(data, list)
    assert len(data) > 0
    os.remove(temp_xml_file)


def test_z_write_data(xml_config):
    """
    Functions to test the write_data function.
    :param xml_config: Configuration class from Pytest fixtures
    """
    retriever = RetrieveXML(xml_config, "xml")
    csvfile = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/CPET702-JOE-BLOGGS.xml"
    )
    output_csv_file = retriever.get_data(csvfile)
    testfile = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/omop_CPET702_data.csv"
    )

    with open(testfile, "r") as expected_file:
        expected_csv_content = expected_file.read()

    with open(output_csv_file, "r") as output_file:
        output_csv_content = output_file.read()

    assert output_csv_content == expected_csv_content

    with open(output_csv_file, "r") as csvfile:
        csv_content = csvfile.read()
        assert any(keyword not in csv_content for keyword in retriever.headers_exclude)

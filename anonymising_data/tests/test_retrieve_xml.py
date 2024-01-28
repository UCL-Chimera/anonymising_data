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
    d = RetrieveXML(xml_config)
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
    retriever = RetrieveXML(xml_config)
    print(xml_directory)

    xml_files = [
        file for file in os.listdir(xml_directory) if file.endswith(".xml")
    ]

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

    retriever = RetrieveXML(xml_config)
    data = retriever.get_xml_data(temp_xml_file)
    assert isinstance(data, list)
    assert len(data) > 0
    os.remove(temp_xml_file)


def test_z_write_data(xml_config):
    """
    Functions to test the write_data function.
    :param xml_config: Configuration class from Pytest fixtures
    """
    dt = [
        [],
        ["CPET Results"],
        [],
        [],
        [],
        ["Patient data"],
        [],
        ["Administrative Data"],
        ["ID", "CPET702"],
        ["Title", "na"],
        ["Last Name", "Bloggs"],
        ["First Name", "Joe"],
        ["Sex", "male"],
        ["Date of Birth", "1969-04-01T00:00:00.000"],
        [],
        [],
        ["Biological and Medical Baseline Data"],
        ["Height", "185 cm"],
        ["Weight", "90.0 kg"],
        [],
        [],
        [],
        [],
        [],
        ["Variable", "Unit", "Rest", "AT", "V'O2peak"],
        ["t", "mm:ss", "00:00 - 03:00", "10:08", "12:16 - 12:46"],
        ["HR", "/min", "73", "116", "143"],
        ["V'O2/HR", "ml", "2.8", "5.9", "7.6"],
        ["V'E", "L/min", "7.3", "21.0", "38.7"],
        [
            "t",
            "Phase",
            "Marker",
            "V'E",
            "PetO2",
            "PetCO2",
            "V'O2",
            "V'CO2",
            "RER",
            "V'E/V'O2",
        ],
        [
            "h:mm:ss.ms",
            "na",
            "na",
            "L/min",
            "mmHg",
            "mmHg",
            "L/min",
            "L/min",
            "na",
            "na",
        ],
        [
            "0:00:09.000",
            "Rest",
            "na",
            "9.9746400000000008",
            "113.4375",
            "32.626785714285703",
            "0.281658226653341",
            "0.23708671288369099",
            "0.84175319748601596",
            "26.175553569304999",
        ],
        [
            "0:00:10.000",
            "Rest",
            "na",
            "9.9746400000000008",
            "113.4375",
            "32.626785714285703",
            "0.281658226653341",
            "0.23708671288369099",
            "0.84175319748601596",
            "26.175553569304999",
        ],
        [],
    ]

    retriever = RetrieveXML(xml_config)
    output_csv_file = retriever.write_data(dt)

    testfile = Path(__file__).parent.parent.joinpath(
        "tests/resources/CPet/test-files/expected-files/omop_person_id_01_cpet_data.csv"
    )

    with open(testfile, "r") as expected_file:
        expected_csv_content = expected_file.read()

    with open(output_csv_file, "r") as output_file:
        output_csv_content = output_file.read()

    assert output_csv_content == expected_csv_content

    with open(output_csv_file, "r") as csvfile:
        csv_content = csvfile.read()
        assert any(
            keyword not in csv_content for keyword in retriever.headers_exclude
        )

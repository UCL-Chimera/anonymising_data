import os
import xml.etree.ElementTree as ET
import csv
from pathlib import Path


class RetrieveXML:
    """
    Class to retrieve data from xml.
    """

    def __init__(self, config):
        self._xml_file = config._database
        self.headers_exclude = config.headers_exclude
        self._output_file = config.omop_data_file
        self._data = None

    @property
    def xml_file(self):
        """
        Returns the path of the xml file.

        :return: The xml file.
        """
        return self._xml_file

    def _getvalueofnode(self, node):
        """return node text or None"""
        return node.text if node is not None else None

    def get_data(self, xml_file):
        """
        Function to get data.
        :return: data from xml
        """
        tree = ET.parse(xml_file)
        root = tree.getroot()

        ns = {"doc": "urn:schemas-microsoft-com:office:spreadsheet"}

        data = []
        for node in root.findall(".//doc:Row", ns):
            row_data = []
            cells = node.findall("doc:Cell", ns)
            for cell in cells:
                data_tag = cell.find("doc:Data", ns)
                if data_tag is not None:
                    cell_data = self._getvalueofnode(data_tag)
                    if cell_data is not None and cell_data.strip():
                        # header = cell_data.split(":")[0].strip()
                        row_data.append(cell_data)
                    else:
                        row_data.append("na")
            data.append(row_data)

        self._data = data
        return data

    def write_data(self):
        """
        A function to output the data retrieved from querying the database.
        If the data has not been read and stored
         this function will call the get_data function.
        """

        xml_files = self._xml_file.glob("*.xml")
        for xml_file in xml_files:
            dt = self.get_data(xml_file)

            xml_filename = os.path.basename(xml_file)
            xml_filename, _ = os.path.splitext(xml_filename)
            new_filename = str(self._output_file).replace(
                "x", str(xml_filename)
            )
            csv_output_file = Path(new_filename)

            with open(csv_output_file, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)

                for row in dt:
                    if len(row) == 2 and ":" in row[0]:
                        row[0] = row[0].replace(":", "")

                    exclude_row = any(
                        exclude_keyword in row or not any(row)
                        for exclude_keyword in self.headers_exclude
                    )

                    if not exclude_row:
                        csv_writer.writerow(row)

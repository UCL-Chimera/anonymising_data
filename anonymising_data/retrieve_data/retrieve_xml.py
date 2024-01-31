import os
import csv
from pathlib import Path

from anonymising_data.utils.check_filename import extract_and_check_format


class RetrieveXML:
    """
    Class to retrieve data from xml.
    """

    def __init__(self, config, data_format):
        self._xml_file = config._xml_data
        self.headers_exclude = config.headers_exclude
        self._output_file = config.omop_data_file
        self._data = None
        self._data_format = data_format

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

    def get_xlsx_data(self, xlsx_filepath):
        """
        Function to get data from an Excel (.xlsx) file.
        :return: data from xlsx
        """
        import openpyxl

        data = []
        workbook = openpyxl.load_workbook(xlsx_filepath)
        sheet = workbook.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_data = []

            for cell_data in row:
                if cell_data is not None:
                    row_data.append(str(cell_data))

            data.append(row_data)

        self._data = data
        return data

    def get_xml_data(self, xml_filepath):
        """
        Function to get data.
        :return: data from xml
        """
        import xml.etree.ElementTree as ET

        tree = ET.parse(xml_filepath)
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
                        row_data.append(cell_data)
                    else:
                        row_data.append("na")
            data.append(row_data)

        self._data = data
        return data

    def get_data(self, xml_filepath):
        if self._data_format == "xlsx":
            data_to_write = self.get_xlsx_data(xml_filepath)
        elif self._data_format == "xml":
            data_to_write = self.get_xml_data(xml_filepath)
        else:
            print("wrong data format")

        xml_filename = os.path.basename(xml_filepath)
        xml_filename, _ = os.path.splitext(xml_filename)

        xml_filename = extract_and_check_format(xml_filename)

        new_filename = str(self._output_file).replace("x", str(xml_filename))
        csv_output_file = Path(new_filename)

        with open(csv_output_file, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)

            for row in data_to_write:
                if len(row) == 2 and ":" in row[0]:
                    row[0] = row[0].replace(":", "")

                exclude_row = any(
                    exclude_keyword in row or not any(row)
                    for exclude_keyword in self.headers_exclude
                )

                if not exclude_row:
                    csv_writer.writerow(row)

        return csv_output_file

    def write_data(self):
        """
        A function to output the data retrieved from querying the database.
        If the data has not been read and stored
         this function will call the get_data function.
        """
        if self._data_format == "xlsx":
            xml_filepaths = self._xml_file.glob("*.xlsx")
        elif self._data_format == "xml":
            xml_filepaths = self._xml_file.glob("*.xml")
        else:
            print("wrong data format")

        xml_filepaths = list(xml_filepaths)
        for xml_filepath in xml_filepaths:
            self.get_data(xml_filepath)

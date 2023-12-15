from pathlib import Path
import xml.etree.ElementTree as ET
import csv


class RetrieveXML:
    """
    Class to retrieve data from xml.
    """

    def __init__(self, config):
        self._xml_file = config._database
        self.headings = config.headers
        # self.pg_connection_string = construct_connection_string(config)
        # if config.sqlserver:
        #     self._conn = MyConnection.create_valid_connection(config.database)
        # else:
        #     self._odbcconn = MyPostgresConnection.create_valid_connection(config.database, self.pg_connection_string)
        #     self._conn = MyPostgresConnection(config.database, self._odbcconn)
        self._output_file = config.omop_data_file
        # self._query = None
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

    def _standardize_dict(self):
        # Check if the dictionary is in the expected structure
        keys = self.headings
        standardized_set = set()
        standardized_dict = {}
        for item in self._data:
            print(item)
            # print("true")
            for key in keys:
                print(key)
                if key in item:
                    standardized_dict[key] = item[key]
                else:
                    standardized_dict.update({v: k for k, v in item.items()})
            standardized_set.add(frozenset(standardized_dict.items()))

        return standardized_set

    def get_data(self):
        """
        Function to get data.
        :return: data from xml
        """
        print(self._xml_file)
        # with open(self._xml_file, 'r') as f:
        #     cfg = yaml.load(f, Loader=yaml.FullLoader)
        # f.close()

        # self._concept_file = Path(__file__).parent.parent.\
        #     joinpath(cfg['files']['input']['concept_mapping']['filename'])

        tree = ET.parse(self._xml_file)
        root = tree.getroot()

        ns = {"doc": "urn:schemas-microsoft-com:office:spreadsheet"}

        # parsed_xml = tree

        data = []
        for node in root.findall(".//doc:Row", ns):
            row_data = []
            cells = node.findall("doc:Cell", ns)
            for cell in cells:
                cell_data = self._getvalueofnode(cell.find("doc:Data", ns))
                if cell_data is not None:
                    row_data.append(cell_data)
            data.append(row_data)

        self._data = data
        print(type(data[0]))
        return data

    def write_data(self):
        """
        A function to output the data retrieved from querying the database.
        If the data has not been read and stored
         this function will call the get_data function.
        """
        dt = self._data if self._data is not None else self.get_data()
        print(self.headings)

        # Extract headers and data rows
        # headers = [cell[0] for cell in dt if len(cell) > 1 and cell[0] != 'Variable']
        # data_rows = [cell[1:] for cell in dt if len(cell) > 1 and cell[0] != 'Variable']

        # print(headers)

        with open(self._output_file, "w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)

            for row in dt:
                for keyword in self.headings:
                    if any(keyword.lower() in cell.lower() for cell in row):
                        csv_writer.writerow(row)
                        break  # If you want to stop after finding the first occurrence in a row

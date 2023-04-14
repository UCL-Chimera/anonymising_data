from pathlib import Path

from anonymising_data.utils.helpers import rreplace


class Query:
    """
    class to read template query file
    and return file with template filled
    """
    def __init__(self, config, concepts):
        self._query_filename = config.query_file
        self._output_query = config.output_query_file
        self._concepts = concepts
        self._con_str = '('
        self._schema = config.schema
        self._offset = config.date_offset
        self._offset_str = ''
        self._testing = config.testing
        self.create_strings()

    def create_strings(self):
        """
        Function to create the strings to be substituted
        """
        for c in self._concepts:
            self._con_str = self._con_str + str(c) + ', '
        self._con_str = rreplace(self._con_str, ', ', ')', 1)
        self._offset_str = str(self._offset)

    def create_query_file(self):
        """
        Function to read template query and substitute values
        """
        with open(self._query_filename, 'r') as f:
            lines = f.readlines()
        f.close()
        num_lines = len(lines)

        # MAKE output dir if necessary

        Path(self._output_query).parent.mkdir(parents=True, exist_ok=True)

        with open(self._output_query, 'w') as out:
            for i in range(0, num_lines):
                out.write(self.adjust_line(lines[i]))
        out.close()

    def adjust_line(self, line):
        """
        Function to take a line
        perform any substitutions if required
        and return
        :param line:
        :return: line with substitutions if any
        """
        if line.find(':FILL_CONCEPT:') != -1:
            newline = line.replace(':FILL_CONCEPT:', self._con_str)
        elif line.find(':FILL_SCHEMA:') != -1:
            if self._testing:
                newline = line.replace(':FILL_SCHEMA:', '')
            else:
                newline = line.replace(':FILL_SCHEMA:', self._schema + '.')
        else:
            newline = line
        return newline

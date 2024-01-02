
class Concepts:
    """
    class to read concept mapping file
    and return the set of concepts to query
    """

    def __init__(self, config):
        self._filename = config.concepts['filename']
        self._concept_index = config.concepts['concept_index']
        self._source_index = config.concepts['source_index']

        self._concepts = []
        self._source = {}

    @property
    def concepts(self):
        """
        Function to return the concepts
        :return: year
        """
        return self._concepts

    @property
    def source(self):
        """
        Function to return the dictionary of concepts and their source.

        :return: source
        """
        return self._source

    def populate_concepts(self):
        """
        Function to read csv and populate list of concept ids
        :return: list of conceptids
        """
        with open(self._filename, 'r') as f:
            lines = f.readlines()
        f.close()
        # put in error checking
        # if not lines[0].startswith('concept_code'):
        num_concepts = len(lines)
        for i in range(1, num_concepts):
            [con_id, source] = self.get_concept_id_and_source(lines[i])
            if con_id != '':
                self._concepts.append(con_id)
                self._source[con_id] = source

    def get_concept_id_and_source(self, line):
        """
        Function to read concept id and source from csv line
        :param line
        :return: [concept id, source]
        """
        parts = line.split(',')
        return [parts[self._concept_index].strip(), parts[self._source_index].strip()]

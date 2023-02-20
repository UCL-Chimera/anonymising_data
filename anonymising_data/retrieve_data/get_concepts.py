from anonymising_data.utils.helpers import FileManager


def get_concept_id(line):
    """
    Function to read concept id from csv line
    :param line:
    :return: concept id
    """
    parts = line.split(',')
    return parts[2].strip()


class Concepts:
    """
    class to read concept mapping file
    and return the set of concepts to query
    """
    def __init__(self, filename):
        self.filename = filename
        self._concepts = []

    @property
    def concepts(self):
        """
        Funcion to return the concepts
        :return: year
        """
        return self._concepts

    def populate_concepts(self):
        """
        Function to read csv and populate list of concept ids
        :return: list of conceptids
        """
        with open(self.filename, 'r') as f:
            lines = f.readlines()
        f.close
            # put in error checking
#            if not lines[0].startswith('concept_code'):
        num_concepts = len(lines)
        for i in range(1, num_concepts):
            self._concepts.append(get_concept_id(lines[i]))


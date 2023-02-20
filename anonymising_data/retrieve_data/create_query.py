class Query:
    """
    class to read template query file
    and return file with template filled
    """
    def __init__(self, config, concepts):
        self._filename = config.query_file
        self._year = config.year
        self._concepts = concepts

#    def create_query_file(self):


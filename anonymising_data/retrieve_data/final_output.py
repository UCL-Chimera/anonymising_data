class Data:
    """
    Class to read omop data and do final data shifting
    """
    def __init__(self, config):
        self._omop_data_file = config.omop_data_file
        self._final_data_file = config.final_data_file

    @property
    def omop_data_file(self):
        """
        Function to return filename of omop data file
        :return:
        """
        return self._omop_data_file

    @property
    def final_data_file(self):
        """
        Function to return filename of final data file
        :return:
        """
        return self._final_data_file




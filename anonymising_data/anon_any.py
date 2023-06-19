from anonymising_data.retrieve_data.final_output import Data
from anonymising_data.retrieve_data.create_query import Query
from anonymising_data.retrieve_data.get_concepts import Concepts
from anonymising_data.retrieve_data.get_config import Config
from anonymising_data.retrieve_data.retrieve_data import RetrieveData


def main():
    """
    Main function

    :return: A csv file containing the anonymised data
    """
    cfg = Config(testing=False)
    cfg.read_yaml()

    data = Data(cfg, None)
    data.final()

    print(f"Anonymised data written to {cfg.vent_headers}")


if __name__ == '__main__':
    main()

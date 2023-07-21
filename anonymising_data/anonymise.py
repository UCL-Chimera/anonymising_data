from anonymising_data.retrieve_data.final_output import Data
from anonymising_data.retrieve_data.create_query import Query
from anonymising_data.retrieve_data.get_concepts import Concepts
from anonymising_data.retrieve_data.get_config import Config
from anonymising_data.retrieve_data.retrieve_data import RetrieveData


def main():
    """
    Main function to run the whole pipeline to anonymise data.

    :return: A csv file containing the anonymised data
    """
    cfg = Config(testing=False)
    cfg.read_yaml()

    con = Concepts(cfg.concept_file)
    con.populate_concepts()

    q = Query(cfg, con.concepts)
    q.create_query_file()

    print(f"Query written to {cfg.output_query_file}")

    d = RetrieveData(cfg)
    d.write_data()

    print(f"Data retrieved from {cfg.schema} written to {cfg.omop_data_file}")

    data = Data(cfg, con._source)
    data.create_final_output()

    print(f"Anonymised data written to {cfg.final_data_file}")


if __name__ == '__main__':
    main()

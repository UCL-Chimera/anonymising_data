from anonymising_data.retrieve_data.create_query import Query
from anonymising_data.retrieve_data.get_concepts import Concepts
from anonymising_data.retrieve_data.get_config import Config


def main():
    cfg = Config(testing=False)
    cfg.read_yaml()

    con = Concepts(cfg.concept_file)
    con.populate_concepts()

    q = Query(cfg, con.concepts)
    q.create_query_file()

    print(f"Query written to {cfg.output_query_file}")


if __name__ == '__main__':
    main()

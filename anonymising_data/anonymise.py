from anonymising_data.retrieve_data.create_query import Query
from anonymising_data.retrieve_data.get_concepts import Concepts
from anonymising_data.retrieve_data.get_config import Config


def main():
    cfg = Config(testing=False)
    cfg.read_yaml()
    print(cfg.concept_file)
    print(cfg.query_file)
    print(cfg.output_query_file)

    con = Concepts(cfg.concept_file)
    con.populate_concepts()

    print(con.concepts)

    q = Query(cfg, con.concepts)
    q.create_query_file()

    print("All done")


if __name__ == '__main__':
    main()

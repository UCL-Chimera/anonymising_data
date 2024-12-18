import argparse


def main(args):
    """
    Main function to run the whole pipeline to anonymise data.
    :param args: The arguements containing test option and data type.
    :return: A csv file containing the anonymised data
    """

    if args.data == "sql":
        from anonymising_data.retrieve_data.final_output import Data
        from anonymising_data.retrieve_data.create_query import Query
        from anonymising_data.retrieve_data.get_concepts import Concepts
        from anonymising_data.retrieve_data.get_config import Config
        from anonymising_data.retrieve_data.retrieve_data import RetrieveData

        cfg = Config(cpet=False, testing=args.testing)
        cfg.read_yaml()

        con = Concepts(cfg)
        con.populate_concepts()

        q = Query(cfg, con.concepts)
        q.create_query_file()

        print(f"Query written to {cfg.output_query_file}")

        d = RetrieveData(cfg, con.concepts)
        d.write_data()

        print(
            f"Data retrieved from {cfg.schema} written to {cfg.omop_data_file}"
        )

        data = Data(cfg, con._source)
        data.create_final_output()

        print(f"Anonymised data written to {cfg.final_data_file}")

    elif args.data == "cpet":
        from anonymising_data.retrieve_data.get_config_cpet import Cpet_Config
        from anonymising_data.retrieve_data.retrieve_xml import RetrieveXML
        from anonymising_data.retrieve_data.final_output_xml import Data

        cfg = Cpet_Config(args.data, testing=args.testing)
        cfg.read_yaml()

        d = RetrieveXML(cfg, args.data_format)
        d.write_data()

        data = Data(cfg, args.data_format)
        data.create_final_output(cfg.final_cpet_data)

        print(f"Demographic data written to {cfg.final_demographic_data}")

    else:
        raise ValueError("Unsupported data type")


def argument_parser() -> argparse.Namespace:
    """
    Parse command-line arguments for the script.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--testing",
        type=bool,
        required=True,
        help="",
    )
    parser.add_argument(
        "--dates",
        type=bool,
        required=True,
        help="",
    )
    parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="sql or cpet",
    )
    parser.add_argument(
        "--data_format",
        type=str,
        default="xlsx",
    )
    return parser.parse_args()


if __name__ == "__main__":
    # import sys
    # sys.path.append(repo_dir)
    args = argument_parser()
    main(args)

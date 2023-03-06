from anonymising_data.retrieve_data.final_output import Data
from anonymising_data.retrieve_data.get_config import Config


def main():
    cfg = Config(testing=False)
    cfg.read_yaml()

    data = Data(cfg)
    data.create_final_output()


if __name__ == '__main__':
    main()

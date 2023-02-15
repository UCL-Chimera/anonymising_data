from anonymising_data.retrieve_data.get_config import Config


def test_create_config():
    cfg = Config()
    assert (cfg.year is None)
    assert (cfg.concept_file == '')
    assert (cfg.query_file == '')


def test_read_config():
    cfg = Config()
    cfg.read_yaml()
    assert (cfg.year == 2023)
    assert (cfg.concept_file ==
            'C:\\Development\\CHIMERA\\data-pipeline-project'
            '\\230214_concept_codes.csv')
    assert (cfg.query_file ==
            'C:\\Development\\CHIMERA\\anonymising_data\\queries'
            '\\omop-es\\get-data.sql')

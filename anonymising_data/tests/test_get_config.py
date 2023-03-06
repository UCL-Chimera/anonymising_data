from pathlib import Path

from anonymising_data.retrieve_data.get_config import Config


def test_create_config():
    """
    Test the Config class is correctly created
    :return:
    """
    cfg = Config()
    assert (cfg.year is None)
    assert (cfg.concept_file == '')
    assert (cfg.query_file == '')
    assert (cfg.database == '')
    assert (cfg.output_query_file == '')
    assert (cfg.omop_data_file == '')
    assert (cfg.final_data_file == '')
    assert (cfg.schema == '')
    assert (cfg.date_offset is None)


def test_read_config():
    """
    Tests the Config class reads correctly from test_config.yml
    :return:
    """
    cfg = Config(testing=True)
    assert (cfg is not None)
    cfg.read_yaml()
    assert (cfg.year == 2000)
    assert (cfg.concept_file == Path(__file__).parent.parent.
            joinpath('tests/resources/test_concept_codes.csv'))
    assert (cfg.query_file == Path(__file__).parent.parent.
            joinpath('tests/resources/test_query.sql'))
    assert (cfg.database == Path(__file__).parent.parent.
            joinpath('tests/resources/mock-database/mock_omop_es.db'))
    assert (cfg.output_query_file == Path(__file__).parent.parent.
            joinpath('tests/output/get_data.sql'))
    assert (cfg.omop_data_file == Path(__file__).parent.parent.
            joinpath('tests/resources/test_data.csv'))
    assert (cfg.final_data_file == Path(__file__).parent.parent.
            joinpath('tests/output/final_data.csv'))
    assert (cfg.schema == 'mock_omop_es')
    assert (cfg.date_offset == 365)

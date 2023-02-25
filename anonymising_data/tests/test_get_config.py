from pathlib import Path

from anonymising_data.retrieve_data.get_config import Config


def test_create_config():
    cfg = Config()
    assert (cfg.year is None)
    assert (cfg.concept_file == '')
    assert (cfg.query_file == '')


def test_read_config():
    cfg = Config(testing=True)
    assert (cfg is not None)
    cfg.read_yaml()
    assert (cfg.year == 2000)
    assert (cfg.concept_file == Path(__file__).parent.parent.
            joinpath('tests/resources/test_concept_codes.csv'))
    assert (cfg.query_file == Path(__file__).parent.parent.
            joinpath('tests/resources/test_query.sql'))
    assert (cfg.output_query_file == Path(__file__).parent.parent.
            joinpath('tests/output/get_data.sql'))
    assert (cfg.omop_data_file == Path(__file__).parent.parent.
            joinpath('tests/resources/test_data.csv'))
    assert (cfg.final_data_file == Path(__file__).parent.parent.
            joinpath('tests/output/final_data.csv'))

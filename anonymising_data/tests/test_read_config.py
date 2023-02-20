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
    # fails on GHA and I need new eyes
    cfg.read_yaml()
    assert (cfg.year == 2000)
    assert (cfg.concept_file == Path('C:/Development/CHIMERA/anonymising_data/'
                                     'anonymising_data/tests/resources/test_concept_codes.csv'))
    assert (cfg.query_file == Path('C:/Development/CHIMERA/anonymising_data/'
                                   'anonymising_data/tests/resources/test_query.sql'))

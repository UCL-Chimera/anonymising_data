from pathlib import Path

from anonymising_data.retrieve_data.get_config import Config


def test_create_config():
    """
    Test the Config class is correctly created
    :return:
    """
    cfg = Config()
    assert (cfg.concept_file == '')
    assert (cfg.query_file == '')
    assert (cfg.database == '')
    assert (cfg.output_query_file == '')
    assert (cfg.omop_data_file == '')
    assert (cfg.final_data_file == '')
    assert (cfg.schema == '')
    assert (cfg.date_offset is None)
    assert (cfg.link_query_file == '')
    assert (cfg.output_link_query_file == '')


def test_read_config():
    """
    Tests the Config class reads correctly from test_config.yml
    :return:
    """
    cfg = Config(testing=True)
    assert (cfg is not None)
    cfg.read_yaml()
    # files input
    assert (cfg.concept_file == Path(__file__).parent.parent.
            joinpath('tests/resources/test_concept_codes.csv'))
    assert (cfg.query_file == Path(__file__).parent.parent.
            joinpath('tests/resources/test_query.sql'))
    assert (cfg.link_query_file == Path(__file__).parent.parent.
            joinpath('tests/resources/link_query.sql'))
    # files output
    assert (cfg.output_query_file == Path(__file__).parent.parent.
            joinpath('tests/output/get_data.sql'))
    assert (cfg.output_link_query_file == Path(__file__).parent.parent.
            joinpath('tests/output/get_link.sql'))
    assert (cfg.omop_data_file == Path(__file__).parent.parent.
            joinpath('tests/output/omop_data.csv'))
    assert (cfg.final_data_file == Path(__file__).parent.parent.
            joinpath('tests/output/final_data.csv'))
    assert (cfg.headers == ["measurement_type", "measurement_source",
                            "person_id", "measurement_datetime",
                            "value_as_number", "units", "value_as_string",
                            "age", "gender", "ethnicity"])
    # database
    assert (cfg.database == Path(__file__).parent.parent.
            joinpath('tests/resources/mock-database/test_omop_es_expanded.sqlite3'))
    assert (cfg.schema == 'mock_omop_es')
    assert (cfg.username == 'fred')
    assert (cfg.password == 'flintstone')
    assert cfg.sqlserver
    assert (cfg.driver == '{some driver}')
    assert (cfg.server == 'some_server')
    assert (cfg.dbname == 'some_database')
    assert (cfg.port == 111)
    # anonymisation
    assert (cfg.date_fields == [3])
    assert (cfg.age_fields == [7])
    assert (cfg.date_offset == 365)
    # concepts
    assert (cfg.concepts['filename'] == cfg.concept_file)
    assert (cfg.concepts['concept_index'] == 2)
    assert (cfg.concepts['source_index'] == 4)

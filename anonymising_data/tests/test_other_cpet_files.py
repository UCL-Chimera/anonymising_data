import filecmp
from pathlib import Path

from anonymising_data.retrieve_data.final_output import Data
from anonymising_data.retrieve_data.create_query import Query
from anonymising_data.retrieve_data.get_concepts import Concepts
from anonymising_data.retrieve_data.get_config import Config

import pytest

from anonymising_data.retrieve_data.retrieve_data import RetrieveData


def test_write_data_cpet_devices():
    """

    :param config: Configuration class from Pytest fixtures
    :return:
    """
    # need correct testing data in our output file
    cfg = Config(cpet=True,testing=True)
    assert (cfg is not None)
    filename = Path(__file__).parent.parent.joinpath('tests', 'resources', 'cpet_ehr_data',
                                                     'test_config_cpet_ehr_devices.yml')
    cfg.set_filename(filename)
    cfg.read_yaml()   
    con = Concepts(cfg)
    con.populate_concepts()

    q = Query(cfg, con.concepts, person_id=con.person_id)
    q.create_query_file()
    newfile = Path(__file__).parent.parent.\
        joinpath('tests/output/get_data_cpet.sql')
    testfile = Path(__file__).parent.parent.\
        joinpath('tests/resources/cpet_ehr_data/expected_get_device_exposure.sql')
    assert (filecmp.cmp(newfile, testfile, shallow=False))
    
    rd = RetrieveData(cfg)
    rd.write_data()
    newfile = Path(__file__).parent.parent.\
        joinpath('tests/output/omop_data_cpet_device.csv')
    testfile = Path(__file__).parent.parent.\
        joinpath('tests/resources/cpet_ehr_data/expected_omop_device.csv')
 
    # now do test
    d = Data(cfg)
    d.create_final_output()
    newfile = Path(__file__).parent.parent.\
        joinpath('tests/output/final_data_cpet_device.csv')
    testfile = Path(__file__).parent.parent.\
        joinpath('tests/resources/cpet_ehr_data/expected_device_data.csv')
    assert (filecmp.cmp(newfile, testfile, shallow=False))


def test_write_data_cpet_drugs():
    """

    :param config: Configuration class from Pytest fixtures
    :return:
    """
    # need correct testing data in our output file
    cfg = Config(cpet=True, testing=True)
    assert (cfg is not None)
    filename = Path(__file__).parent.parent.joinpath('tests', 'resources', 'cpet_ehr_data',
                                                     'test_config_cpet_ehr_drugs.yml')
    cfg.set_filename(filename)
    cfg.read_yaml()
    con = Concepts(cfg)
    con.populate_concepts()

    q = Query(cfg, con.concepts, person_id=con.person_id)
    q.create_query_file()
    newfile = Path(__file__).parent.parent. \
        joinpath('tests/output/get_data_cpet.sql')
    testfile = Path(__file__).parent.parent. \
        joinpath('tests/resources/cpet_ehr_data/expected_get_drug_exposure.sql')
    assert (filecmp.cmp(newfile, testfile, shallow=False))

    rd = RetrieveData(cfg)
    rd.write_data()
    newfile = Path(__file__).parent.parent. \
        joinpath('tests/output/omop_data_cpet_drug.csv')
    testfile = Path(__file__).parent.parent. \
        joinpath('tests/resources/cpet_ehr_data/expected_omop_drug.csv')

    # now do test
    d = Data(cfg)
    d.create_final_output()
    newfile = Path(__file__).parent.parent. \
        joinpath('tests/output/final_data_cpet_drug.csv')
    testfile = Path(__file__).parent.parent. \
        joinpath('tests/resources/cpet_ehr_data/expected_drug_data.csv')
    assert (filecmp.cmp(newfile, testfile, shallow=False))


def test_write_data_cpet_admission():
    """

    :param config: Configuration class from Pytest fixtures
    :return:
    """
    # need correct testing data in our output file
    cfg = Config(cpet=True, testing=True)
    assert (cfg is not None)
    filename = Path(__file__).parent.parent.joinpath('tests', 'resources', 'cpet_ehr_data',
                                                     'test_config_cpet_ehr_admission.yml')
    cfg.set_filename(filename)
    cfg.read_yaml()
    con = Concepts(cfg)
    con.populate_concepts()

    q = Query(cfg, con.concepts, person_id=con.person_id)
    q.create_query_file()
    newfile = Path(__file__).parent.parent. \
        joinpath('tests/output/get_data_cpet.sql')
    testfile = Path(__file__).parent.parent. \
        joinpath('tests/resources/cpet_ehr_data/expected_get_hospital_stay.sql')
    assert (filecmp.cmp(newfile, testfile, shallow=False))

    rd = RetrieveData(cfg)
    rd.write_data()
    newfile = Path(__file__).parent.parent. \
        joinpath('tests/output/omop_data_cpet_admission.csv')
    testfile = Path(__file__).parent.parent. \
        joinpath('tests/resources/cpet_ehr_data/expected_omop_admission.csv')

    # now do test
    d = Data(cfg)
    d.create_final_output()
    newfile = Path(__file__).parent.parent. \
        joinpath('tests/output/final_data_cpet_admission.csv')
    testfile = Path(__file__).parent.parent. \
        joinpath('tests/resources/cpet_ehr_data/expected_admission_data.csv')
    assert (filecmp.cmp(newfile, testfile, shallow=False))
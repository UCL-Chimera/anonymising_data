import pytest
from retrieve_data.retrieve_data import RetrieveData


@pytest.fixture(scope='module')
def retrieval():
    return RetrieveData('caboodle', 'patientTemp')

from pathlib import Path

from anonymising_data.retrieve_data.get_concepts import Concepts
from anonymising_data.retrieve_data.get_concepts import get_concept_id

import pytest


def test_create_concepts(concept_file):
    con = Concepts(concept_file)
    assert (con is not None)
    assert (con.filename == Path(__file__).parent.parent.
            joinpath('tests/resources/test_concept_codes.csv'))


@pytest.mark.parametrize("line, concept_id", [
    ('400, SNOMED, 432, Body temperature, Measurement', '432'),
    ('12 - Jul, LOINC, 543, Oxygen[Partial pressure], Measurement', '543'),
])
def test_get_concept(line, concept_id):
    assert (get_concept_id(line) == concept_id)


def test_get_concepts(concept_file):
    con = Concepts(concept_file)
    con.populate_concepts()
    assert (con.concepts == ['1', '23', '5872'])

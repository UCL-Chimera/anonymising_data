import pytest

from anonymising_data.linking.get_person_id import Link


@pytest.mark.parametrize("mrn, person_id", [
    ('d4wr5', 1),
    ('12345', 6327),
    ('sd/678', 7341),
    ('.345', None)
    #('Female', [(6327,)])
])
def test_get_person_id(config, mrn, person_id):
    link = Link(config)
    assert (link.get_person_id(mrn) == person_id)
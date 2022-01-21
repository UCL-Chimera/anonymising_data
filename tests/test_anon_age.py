import pytest
from anonymising_data.age import Age


@pytest.mark.parametrize("age, anon_age", [
    (3, 3
     ),
])
def test_anonymise_age(age, anon_age):
    assert(age == anon_age)



@pytest.mark.parametrize("dob, days, months, years, testdate", [
    ('2022-1-1', 19, 0, 0, '2022-1-20'),
    ('1993-01-3', 17, 0, 29, '2022-1-20'),
    ('1960-07-27', 2, 0, 49, '2009-07-29'),
    ('1960-07-27', 0, 11, 48, '2009-06-27'),
    ('1960-07-27', 0, 0, 49, '2009-07-27'),
    ('1960-07-27', 0, 1, 49, '2009-08-27'),
    ('1960-07-27', 2, 1, 49, '2009-08-29'),
    ('1960-07-27', 13, 11, 48, '2009-07-10'),
    ('1960-12-27', 13, 9, 48, '2009-10-10'),
    ('1960-12-27', 13, 9, 39, '2000-10-10'),
    ('1960-2-27', 12, 0, 40, '2000-3-10'),

])
def test_calculate_age(dob, days, months, years, testdate):
    age = Age(dob)
    age.calculate_age_for_testing(testdate)
    assert (age.get_days() == days)
    assert (age.get_months() == months)
    assert (age.get_years() == years)

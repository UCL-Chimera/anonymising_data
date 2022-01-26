import pytest
from anonymising_data.age import Age


@pytest.mark.parametrize("dob, days, months, years, testdate", [
    ('2022-1-1', 19, 0, 0, '2022-1-20'),
    ('1993-01-3', 17, 0, 29, '2022-1-20'),
    ('1960-07-27', 2, 0, 49, '2009-07-29'),
    ('1960-07-27', 0, 11, 48, '2009-06-27'),
    ('1960-07-27', 0, 0, 49, '2009-07-27'),
    ('1960-07-27', 0, 1, 49, '2009-08-27'),
    ('1960-07-27', 2, 1, 49, '2009-08-29'),
    ('1960-07-27', 14, 0, 49, '2009-08-10'),
    ('1960-07-27', 13, 11, 48, '2009-07-10'),
    ('1960-12-27', 13, 9, 48, '2009-10-10'),
    ('1960-12-27', 13, 9, 39, '2000-10-10'),
    ('1960-2-27', 12, 0, 40, '2000-3-10'),
    ('2000-2-10', 10, 11, 19, '2020-1-20'),
    ('2000-2-10', 10, 0, 20, '2020-2-20'),
])
def test_calculate_age(dob, days, months, years, testdate):
    """
    Tests that the calculate age function works as expected

    :param dob: date of birth
    :param testdate: date to calculate age

    :param days: expected age days
    :param months: expected age months
    :param years: expected age years
    """
    age = Age(dob)
    age.calculate_age_for_testing(testdate)
    assert (age.get_days() == days)
    assert (age.get_months() == months)
    assert (age.get_years() == years)


@pytest.mark.parametrize("dob, testdate, anon_age", [
    ('2000-2-10', '2000-2-20', 1),
    ('2000-2-10', '2000-6-20', 19),
    ('2000-2-10', '2000-9-23', 32),
    ('2000-2-10', '2001-2-03', 51),
    ('2000-2-10', '2001-2-20', 12),
    ('2000-2-10', '2010-2-20', 120),
    ('2000-2-10', '2010-3-09', 121),
    ('2000-2-10', '2010-2-20', 120),
    ('2000-10-10', '2018-3-09', 209),
    ('1993-01-3', '2022-1-20', 29),
    ('1960-07-27', '2009-07-29', 49),
    ('1960-12-27', '2009-10-10', 49),
    ('1960-12-27', '2000-10-10', 40),
    ('1960-2-27', '2000-3-10', 40),
    ('2000-2-10', '2020-1-20', 20),
    ('2000-2-10', '2020-7-20', 20),
    ('2000-2-10', '2020-7-30', 21),
    ('2000-2-10', '2098-3-20', 98),
    ('2000-2-10', '2099-3-20', 100),
    ('2000-2-10', '2099-1-20', 99),
])
def test_anonymise_age(dob, testdate, anon_age):
    """
    Test to check anonymise age works as expected
    :param dob: date of birth
    :param testdate: date to calculate age
    :param anon_age: expected anonymised age
    :return:
    """
    age = Age(dob)
    age.anonymise_age_for_testing(testdate)
    assert(age.get_anon_age() == anon_age)

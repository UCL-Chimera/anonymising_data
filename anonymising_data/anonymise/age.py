from datetime import datetime
from dateutil.relativedelta import relativedelta

# todo note need to record date used to anon
from anonymising_data.utils.helpers import create_date


class Age:
    """
    Class to calculate age and anonymise
    """

    def __init__(self, dob, testing=False):
        # leave out time if present
        self.dob = create_date(dob)
        self._days = None
        self._months = None
        self._years = None
        self.total_days = -1
        self._anon_age = None
        self._testing = testing
        self.testdate = None
        if testing:
            self.testdate = '2023-12-22'
        self.__anonymise_age()

    @property
    def anon_age(self):
        """
        Function to return anonymsied age.
        :return: self.anon_age
        """
        return self._anon_age

    @property
    def days(self):
        """
        Function to return age in days.
        :return:
        """
        return self._days

    @property
    def months(self):
        """
        Function to return age in months.
        :return:
        """
        return self._months

    @property
    def years(self):
        """
        Function to return age in years.
        :return:
        """
        return self._years

    def calculate_age_for_testing(self, strdate):
        """
        Function taking a dummy date as today for testing.
        :param strdate: dummy date as string YYYY-M-D
        """
        self.__calculate_age(strdate)

    def anonymise_age_for_testing(self, strdate):
        """
        Function taking a dummy date as today for testing.
        :param strdate: dummy date as string YYYY-M-D
        """
        self.__anonymise_age(strdate)

    def __calculate_age(self, test_date=None):
        """
        Function to calculate age using date of birth and todays date.
        :param test_date dummy date used as 'today' for tests
        """
        if not test_date:
            if self._testing:
                reference_date = datetime.strptime(self.testdate, '%Y-%m-%d')
            else:
                reference_date = datetime.today()
        else:
            reference_date = datetime.strptime(test_date, '%Y-%m-%d')

        self.total_days = (reference_date - self.dob).days

        rdiff = relativedelta(reference_date, self.dob)
        self._years = rdiff.years
        self._months = rdiff.months
        self._days = rdiff.days

    def __anonymise_age(self, test_date=None):
        """
        Function to anonymise age.
        :param test_date dummy date used as 'today' for tests
        :return: age in weeks if < 1 yr
                     in months if < 18 yrs
                     in years if < 99 yrs
                     100 otherwise
        """
        self.__calculate_age(test_date)
        if self.years == 0:
            self._anon_age = round(self.total_days / 7, 0)
        elif self.years < 18:
            round_up_days = self.days > 15
            self._anon_age = (self.years * 12) + self.months + round_up_days
        elif self.years < 99:
            round_up_days = self.days > 15
            round_up_months = (self.months + round_up_days) > 5
            self._anon_age = self.years + round_up_months
        else:
            self._anon_age = 100

from datetime import datetime
from dateutil.relativedelta import *

# todo note need to record date used to anon


class Age:
    """
    Class to calculate age and anonymise
    """

    def __init__(self, dob):
        self.dob = datetime.strptime(dob, '%Y-%m-%d')
        self.days = -1
        self.months = -1
        self.years = -1
        self.total_days = -1
        self.anon_age = -1
        self.__anonymise_age()

    def get_anon_age(self):
        """
        Function to return anonymsied age
        :return: self.anon_age
        """
        return self.anon_age

    def get_days(self):
        """
        Funcion to return age in days
        :return:
        """
        return self.days

    def get_months(self):
        """
        Funcion to return age in months
        :return:
        """
        return self.months

    def get_years(self):
        """
        Funcion to return age in years
        :return:
        """
        return self.years

    def calculate_age_for_testing(self, strdate):
        """
        Function taking a dummy date as today for testing
        :param strdate: dummy date as string YYYY-M-D
        """
        self.__calculate_age(strdate)

    def anonymise_age_for_testing(self, strdate):
        """
        Function taking a dummy date as today for testing
        :param strdate: dummy date as string YYYY-M-D
        """
        self.__anonymise_age(strdate)

    def __calculate_age(self, testdate=None):
        """
        Function to calculate age using date of birth and todays date
        :param testdate dummy date used as 'today' for tests
        """
        if not testdate:
            reference_date = datetime.today()
        else:
            reference_date = datetime.strptime(testdate, '%Y-%m-%d')

        self.total_days = (reference_date - self.dob).days
        
        rdiff = relativedelta(reference_date, self.dob)
        self.years = rdiff.years
        self.months = rdiff.months
        self.days = rdiff.days

    def __anonymise_age(self, testdate=None):
        """
        Function to anonymise age
        :param testdate dummy date used as 'today' for tests
        :return: age in weeks if < 1 yr
                     in months if < 18 yrs
                     in years if < 99 yrs
                     100 otherwise
        """
        self.__calculate_age(testdate)
        if self.years == 0:
            self.anon_age = round(self.total_days / 7, 0)
        elif self.years < 18:
            round_up_days = self.days > 15
            self.anon_age = (self.years * 12) + self.months + round_up_days
        elif self.years < 99:
            round_up_days = self.days > 15
            round_up_months = (self.months + round_up_days) > 5
            self.anon_age = self.years + round_up_months
        else:
            self.anon_age = 100

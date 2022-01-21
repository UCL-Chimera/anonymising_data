from datetime import date, datetime

days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


#todo note need to record date used to anon

class Age:
    """
    Class to calculate age and anonymise
    """
    def __init__(self, dob):
        self.dob = datetime.strptime(dob, '%Y-%m-%d')
        self.days = 0
        self.months = 0
        self.years = 0
        self.total_days = 0
        self.anon_age = self.__anonymise_age()

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
            today = datetime.today()
        else:
            today = datetime.strptime(testdate, '%Y-%m-%d')

        # work out whether we have had a birthday this year
        # i.e. your dob is xxx-07-27 and today is xxx-02-16 you have not reached the 2nd month or the 27th
        reached_month_of_birthday = (today.month >= self.dob.month)
        birthday_this_month = today.month == self.dob.month
        reached_day_of_birthday = (today.day >= self.dob.day)
        had_birthday_this_year = reached_day_of_birthday if birthday_this_month else reached_month_of_birthday

        self.total_days = (today - self.dob).days
        self.years = today.year - self.dob.year - (not had_birthday_this_year)

        if had_birthday_this_year:
            if reached_day_of_birthday:
                self.days = today.day - self.dob.day
                self.months = today.month - self.dob.month
            else:
                self.days = self._end_of_last_month(today.month - 1, today.year, self.dob.day) + today.day
                self.months = today.month - self.dob.month -1
        else:
            if reached_day_of_birthday:
                self.months = 12 + today.month - self.dob.month
                self.days = today.day - self.dob.day
            else:
                self.months = 11 + today.month - self.dob.month
                self.days = self._end_of_last_month(today.month - 1, today.year, self.dob.day) + today.day

    def _end_of_last_month(self, month, year, day):
        """
        Function to calculate days from last month when day of birth has not been reached in current month

        e.g. dob is 1960-07-27 today is 2009-08-10
        age is 49 yrs 0 months and 14 days(4 from end July + 10 from Aug)
        :param month: index of month in array
        :param year: todays year
        :param day: dob day
        :return: number of days in last month from day of birth e.g. 4 in example
        """
        days = days_in_months[month-1] - day
        if self._is_leap_year(year) and month == 2:
            days = days + 1
        return days

    @staticmethod
    def _is_leap_year(year):
        """
        Predicate indicating that a year is a leap year of not
        :param year: year
        :return: True if leap year, False otherwise
        """
        return (year % 4) == 0

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
            self.anon_age = round(self.total_days/7, 0)
        elif self.years < 18:
            round_up_days = self.days > 15
            self.anon_age = (self.years * 12) + self.months + round_up_days
        elif self.years < 99:
            round_up_days = self.days > 15
            round_up_months = (self.months + round_up_days) > 5
            self.anon_age = self.years + round_up_months
        else:
            self.anon_age = 100



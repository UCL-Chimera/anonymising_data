from datetime import date, datetime


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
        self.__calculate_age()
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

    def __calculate_age(self, testdate=None):
        """
        Function to calculate age from date of birth
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

        self.years = today.year - self.dob.year - (not had_birthday_this_year)

        if had_birthday_this_year:
            if reached_day_of_birthday:
                self.days = today.day - self.dob.day
                self.months = today.month - self.dob.month
            else:
                self.days = self._end_of_last_month(today.month - 1, today.year, self.dob.day) + today.day
                self.months = today.month - self.dob.month -1
        else:
            self.months = 11 + today.month - self.dob.month
            if reached_day_of_birthday:
                self.months = 12 + today.month - self.dob.month
                self.days = today.day - self.dob.day
            else:
                self.months = 11 + today.month - self.dob.month
                self.days = self._end_of_last_month(today.month - 1, today.year, self.dob.day) + today.day

    def _end_of_last_month(self, month, year, day):
        days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        days = days_in_months[month-1] - day
        if self._is_leap_year(year) and month == 2:
            days = days + 1
        return days

    def _is_leap_year(self, year):
        return (year % 4) == 0

    def calculate_age_for_testing(self, strdate):
        self.__calculate_age(strdate)

    def __anonymise_age(self):
        """
        Function to anonymise age
        :return: age in weeks if < 1 yr
                     in months if < 18 yrs
                     in years if < 99 yrs
                     100 otherwise
        """
        anon_age = 3
        return anon_age

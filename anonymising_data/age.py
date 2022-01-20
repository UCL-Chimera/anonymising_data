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
            today = date.today()
        else:
            today = datetime.strptime(testdate, '%Y-%m-%d')
        # work out whether we have had a birthday this year
        # i.e. your dob is xxx-07-27 and today is xxx-02-16 you have not reached the 2nd month or the 27th
        reached_month_of_birthday = (today.month >= self.dob.month)
        reached_day_of_birthday = (today.day >= self.dob.day)
        had_birthday_this_year = reached_month_of_birthday and reached_day_of_birthday

        self.years = today.year - self.dob.year - (not had_birthday_this_year)

        if had_birthday_this_year:
            self.months = today.month - self.dob.month
        else:
            self.months = 12 + today.month - self.dob.month
        self.days = today.day - self.dob.day

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

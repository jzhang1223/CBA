import CalculationAPI
import datetime

# Converts datetime.date to and string date, and vice versa. Throws error if None or a different data type is given.
class ConvertDate(CalculationAPI.CalculationAPI):

    def __call__(self, date):
        if type(date) == datetime.date:
            return "{}-{}-{}".format(date.year, date.month, date.day)
        elif type(date) == str:
            return datetime.datetime.strptime(date, '%y-%m-%d')
        else:
            raise ValueError("Requires a datetime.date or str")

#a = ConvertDate()
#b = datetime.date(2012, 1, 4)
#c = "11-03-30"
#print a(b)
#print a(c)
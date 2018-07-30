
from Calculations import CalculationAPI

class Nav(CalculationAPI.CalculationAPI):


    def __call__(self, fundID, endDate, startDate=0):
        # should query the db to return the table from startDate to endDate with LIKE fundID
        cursor = "TODO: get the table cursor"
        self.calculate(cursor)

    def calculate(self, cursor):
        # calculate nav from from ROC, income, contributions
        print "TODO"


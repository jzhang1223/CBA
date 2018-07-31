
from Calculations import CalculationAPI

class Nav(CalculationAPI.CalculationAPI):


    def __call__(self, fundID, endDate, startDate=0):

        print self.CashFlowDB.queryDB(
            "SELECT totalNav(\'" + fundID + "\',\'" + endDate + "\')").fetchone()

    def giveResult(self, result):
        # calculate nav from from ROC, income, contributions
        print "TODO"

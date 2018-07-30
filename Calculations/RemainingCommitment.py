import CalculationAPI
from Classes import Query

class RemainingCommitment(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):
        print self.CashFlowDB.queryDB(
            "SELECT remainingCommitment(\'" + fundID + "\',\'" + endDate + "\')").fetchone()

    def calculate(self, cursor, endDate):
        pass



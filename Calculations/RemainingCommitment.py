import CalculationAPI
from Classes import Query

class RemainingCommitment(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):

        result = self.CashFlowDB.queryDB(
            "SELECT remainingCommitment(\'" + fundID + "\',\'" + endDate + "\')").fetchone()[0]

        return self.giveResult(result)




import CalculationAPI

class TotalDistributions(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):
        return self.CashFlowDB.queryDB(
            "SELECT totalDistributions(\'" + fundID + "\',\'" + endDate + "\')").fetchone()[0]

    def giveResult(self, result):
        pass

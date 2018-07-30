import CalculationAPI

class TotalDistributions(CalculationAPI.CalculationAPI):
    def __call__(self, fundID, endDate):
        print self.CashFlowDB.queryDB(
            "SELECT totalDistributions(\'" + fundID + "\',\'" + endDate + "\')").fetchone()[0]
    def calculate(self, cursor, endDate):
        pass
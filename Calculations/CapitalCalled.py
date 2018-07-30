import CalculationAPI

class CapitalCalled(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):
        print self.CashFlowDB.queryDB(
            "SELECT capitalCalled(\'" + fundID + "\',\'" + endDate + "\')").fetchone()[0]

    def calculate(self, cursor, endDate):
        pass
import CalculationAPI

class CapitalCalled(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):

        result = self.CashFlowDB.queryDB(
            "SELECT capitalCalled(\'" + fundID + "\',\'" + endDate + "\')").fetchone()[0]

        return self.giveResult(result)



a = CapitalCalled()
a('CCDD062016AF', '18/4/2')
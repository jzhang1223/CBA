import CalculationAPI

class CapitalCommited(CalculationAPI.CalculationAPI):

    def __call__(self, fundID):

        result = self.CashFlowDB.queryDB(
            "SELECT capitalCommited(\'" + fundID + "\')").fetchone()[0]

        return self.giveResult(result)

a = CapitalCommited()
a('CCDD062016AF')
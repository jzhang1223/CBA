import CalculationAPI

class FundStartDate(CalculationAPI.CalculationAPI):

    def __call__(self, fundID):

    #select fundStartDate('TBPE112014AF');
        result = self.CashFlowDB.queryDB(
            "SELECT fundStartDate(\'{}\');".format(fundID)).fetchone()[0]
        return self.giveResult(result)

a = FundStartDate()
a('TBPE112014AF')

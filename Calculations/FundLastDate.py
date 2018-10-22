import CalculationAPI

class FundLastDate(CalculationAPI.CalculationAPI):

    def __call__(self, fundID):

        result = self.CashFlowDB.queryDB(
            "SELECT fundEndDate(\'{}\');".format(fundID)).fetchone()[0]
        return self.giveResult(result)

a = FundLastDate()
a('TBPE112014AF')
import CalculationAPI

class CapitalCommited(CalculationAPI.CalculationAPI):

    def __call__(self, fundID):
        print self.CashFlowDB.queryDB(
            "SELECT capitalCommited(\'" + fundID + "\')").fetchone()[0]
    def calculate(self, cursor, endDate):
        pass

a = CapitalCommited()
a('BCPE112014')
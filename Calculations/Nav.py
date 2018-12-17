from Calculations import CalculationAPI

class Nav(CalculationAPI.CalculationAPI):


    def __call__(self, fundID, endDate):

        result = self.CashFlowDB.queryDB(
            "SELECT totalNav(\'" + fundID + "\',\'" + endDate + "\')").fetchone()[0]

        return self.giveResult(result)


#a = Nav()
#a('CCDD062016AF', '18/4/2')

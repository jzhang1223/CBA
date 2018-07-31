import CalculationAPI
import TotalDistributions
import Nav

class TotalValue(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):
        nav = Nav.Nav()

        distributions = TotalDistributions.TotalDistributions()

        result = nav(fundID, endDate) + distributions(fundID, endDate)
        return self.giveResult(result)

a = TotalValue()
a('CCDD062016AF', '18/4/2')
import CalculationAPI
import TotalDistributions
import CapitalCalled

class Dpi(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, dateInQtr):

        distributions = TotalDistributions.TotalDistributions()

        called = CapitalCalled.CapitalCalled()

        result = (.00 + distributions(fundID, dateInQtr)) / called(fundID, dateInQtr)
        return self.giveResult(result)

a = Dpi()
a('CCDD062016AF', '18/4/2')
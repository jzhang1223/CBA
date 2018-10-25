import CalculationAPI
from TotalDistributions import TotalDistributions
from CapitalCalled import CapitalCalled

class Dpi(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, dateInQtr):

        distributions = TotalDistributions()

        called = CapitalCalled()

        result = (.00 + distributions(fundID, dateInQtr)) / called(fundID, dateInQtr)
        return self.giveResult(result)

#a = Dpi()
#a('CCDD062016AF', '18/4/2')
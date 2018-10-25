import CalculationAPI
from TotalValue import TotalValue
from CapitalCalled import CapitalCalled

class Tvpi(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, dateInQtr):

        totalValue = TotalValue()

        capitalCalled = CapitalCalled()

        result = (.00 + totalValue(fundID, dateInQtr)) / capitalCalled(fundID, dateInQtr)
        return self.giveResult(result)


#a = Tvpi()
#a('CCDD062016AF', '18/4/2')
import CalculationAPI
import TotalValue
import CapitalCalled

class Tvpi(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, dateInQtr):

        totalValue = TotalValue.TotalValue()

        capitalCalled = CapitalCalled.CapitalCalled()

        result = (.00 + totalValue(fundID, dateInQtr)) / capitalCalled(fundID, dateInQtr)
        return self.giveResult(result)

a = Tvpi()
a('CCDD062016AF', '18/4/2')
import CalculationAPI
from CapitalCommited import CapitalCommited
from CapitalCalled import CapitalCalled

class CalledPercentage(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):
        called = CapitalCalled()

        commited = CapitalCommited()

        result =  (.00 + called(fundID, endDate)) / commited(fundID)
        return self.giveResult(result)

a = CalledPercentage()
a('CCDD062016AF', '18/4/2')
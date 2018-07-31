import CalculationAPI
import CapitalCommited
import CapitalCalled

class CalledPercentage(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):
        called = CapitalCalled.CapitalCalled()

        commited = CapitalCommited.CapitalCommited()

        result =  (.00 + called(fundID, endDate)) / commited(fundID)
        return self.giveResult(result)

a = CalledPercentage()
a('CCDD062016AF', '18/4/2')
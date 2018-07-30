import CalculationAPI
import CapitalCommited
import CapitalCalled

class CalledPercentage(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):
        called = CapitalCalled()

        commited = CapitalCommited()

        return called(fundID, endDate) / commited(fundID)

    def calculate(self, cursor, endDate):
        pass
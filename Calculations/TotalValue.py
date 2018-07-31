import CalculationAPI
import TotalDistributions
import Nav

class TotalValue(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):
        nav = Nav()

        distributions = TotalDistributions()

        return nav(fundID, endDate) + distributions(fundID, endDate)

    def giveResult(self, result):
        pass
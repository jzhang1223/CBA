import CalculationAPI
import TotalDistributions
import Nav

class TotalValue(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, endDate):
        nav = Nav()

        Distributions = TotalDistributions()

        return nav(fundID, endDate) + Distributions(fundID, endDate)

    def calculate(self, cursor, endDate):
        pass
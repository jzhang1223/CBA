import CalculationAPI
from TotalValue import TotalValue
from CapitalCommited import CapitalCommited


class Tvcc(CalculationAPI.CalculationAPI):

    def __call__(self, fundID, dateInQtr):

        totalValue = TotalValue()

        capitalCommited = CapitalCommited()

        result = (.00 + totalValue(fundID, dateInQtr)) / capitalCommited(fundID)
        return self.giveResult(result)


#a = Tvcc()
#a('TBPE112014AF', '18/8/1')


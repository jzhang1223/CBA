from APIs import FundAPI


class Fund(FundAPI.FundAPI):

    # String
    #fundID = None
    # tbd
    #currency = None

    def __init__(self, fundID, currency):
        self.fundID = fundID
        self.currency = currency

    def getID(self):
        return self.fundID

    def getCurrency(self):
        return self.currency
from APIs import CashFlowAPI

class CashFlow(CashFlowAPI):
    cfID = None
    fundID = None
    date = None
    value = None
    typeID = None
    notes = None

    def __init__(self, cfID, fundID, date, value, typeID, notes):
        self.cfID = cfID
        self.fundID = fundID
        self.date = date
        self.value = value
        self.typeID = typeID
        self.notes = notes

    def getID(self):
        return self.fundID

    def getFundID(self):
        return self.currency

    def getDate(self):
        return self.fundID

    def getCurrency(self):
        return self.currency

    def getTypeID(self):
      return self.fundID

    def getCurrency(self):
        return self.currency

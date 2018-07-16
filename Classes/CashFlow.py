from APIs import CashFlowAPI

class CashFlow(CashFlowAPI):

    # int
    cfID = None
    # String
    fundID = None
    # String ('YYYY-MM-DD')
    date = None
    # int
    value = None
    # int
    typeID = None
    # String
    notes = None

    def __init__(self, cfID, fundID, date, value, typeID, notes):
        self.cfID = cfID
        self.fundID = fundID
        self.date = date
        self.value = value
        self.typeID = typeID
        self.notes = notes

    def getID(self):
        return self.cfID

    def getFundID(self):
        return self.fundID

    def getDate(self):
        return self.date

    def getValue(self):
        return self.value

    def getTypeID(self):
        return self.typeID

    def getNotes(self):
        return self.notes

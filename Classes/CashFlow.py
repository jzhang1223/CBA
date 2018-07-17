from APIs import CashFlowAPI

class CashFlow(CashFlowAPI.CashFlowAPI):

    # String
    fundID = None
    # Datetime.Datetime -> String ('YYYY-MM-DD')
    date = None
    # int
    value = None
    # int
    typeID = None
    # String
    notes = None

    def __init__(self, fundID, date, value, typeID, notes):
        self.fundID = fundID
        self.date = date
        self.value = value
        self.typeID = typeID
        self.notes = notes

    def getFundID(self):
        return self.fundID

    # Formats date object into sql's yyyy-mm-dd format
    def getDate(self):
        return str(self.date.year) + "/" + str(self.date.month) + "/" + str(self.date.day)

    def getValue(self):
        return self.value

    def getTypeID(self):
        return self.typeID

    def getNotes(self):
        return self.notes

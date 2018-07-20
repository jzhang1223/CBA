class CashFlowAPI(object):

    # Foreign key
    def getFundID(self):
        return NotImplementedError("Abstract Class")

    def getDate(self):
        return NotImplementedError("Abstract Class")

    def getValue(self):
        return NotImplementedError("Abstract Class")

    # Foreign key
    def getTypeID(self):
        return NotImplementedError("Abstract Class")

    def getNotes(self):
        return NotImplementedError("Abstract Class")

    def sameCashFlow(self, other):
        return NotImplementedError("Abstract Class")
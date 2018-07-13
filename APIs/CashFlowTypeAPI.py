class CashFlowTypeAPI(object):

    # Primary key
    def getID(self):
        return NotImplementedError("Abstract Class")

    def getResult(self):
        return NotImplementedError("Abstract Class")

    def getUse(self):
        return NotImplementedError("Abstract Class")
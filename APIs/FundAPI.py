class FundAPI(object):

    # Primary key
    def getID(self):
        return NotImplementedError("Abstract Class")

    def getCurrency(self):
        return NotImplementedError("Abstract Class")
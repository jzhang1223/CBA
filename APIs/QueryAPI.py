class QueryAPI(object):
    # Signatures not yet compelete
    # Simple Functions
    def getFundTransactions(self, fund):
        return NotImplementedError("Abstract Class")

    # Calculated Functions
    # Possible use of higher order functions here?
    def remainingCommitment(self, fundID):
        return NotImplementedError("Abstract Class")
    def currentNAV(self, fundID):
        return NotImplementedError("Abstract Class")
    def getGrowth(self, fundID):
        return NotImplementedError("Abstract Class")
from APIs import ControllerAPI

class Controller(ControllerAPI.ControllerAPI):

    def getFundTransactions(self, fund):
        return NotImplementedError("Todo")


    def remainingCommitment(self, fundID):
        return NotImplementedError("Todo")
    def currentNAV(self, fundID):
        return NotImplementedError("Todo")
    def getGrowth(self, fundID):
        return NotImplementedError("Todo")
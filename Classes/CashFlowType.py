from APIs import CashFlowTypeAPI

class CashFlowType(CashFlowTypeAPI.CashFlowTypeAPI):

    cftID = None
    result = None
    use = None

    def __init__(self, cftID, result, use):
        self.cftID = cftID
        self.result = result
        self.use = use

    def getID(self):
        return self.cftID

    def getResult(self):
        return self.result

    def getUse(self):
        return self.use
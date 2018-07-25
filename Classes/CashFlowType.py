from APIs import CashFlowTypeAPI

class CashFlowType(CashFlowTypeAPI.CashFlowTypeAPI):

    # Int
    #cftID = None
    # 'Distribution' or 'Contribution'
    #result = None
    # String
    #useCase = None

    def __init__(self, cftID, result, use):
        self.cftID = cftID
        self.result = result
        self.use = use

    def getID(self):
        return self.cftID

    def getResult(self):
        return self.result

    def getUseCase(self):
        return self.useCase
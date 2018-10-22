from Classes import Query

class CalculationAPI(object):

    CashFlowDB = Query.Query()

    # Generic function to allow for a specific calculation of the data.
    def giveResult(self, result):
        #print result
        if result is None:
            return 0
        return result

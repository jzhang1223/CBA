from Classes import Query

class CalculationAPI(object):

    CashFlowDB = Query.Query()

    # Generic function to allow for a specific calculation of the data.
    def calculate(self, cursor, endDate):
        return NotImplementedError("Abstract Class")

from Classes import Query

class CalculationAPI(object):

    CashFlowDB = Query.Query()

    # Generic function to allow for a specific calculation of the data.
    def calculate(self, cursor):
        return NotImplementedError("Abstract Class")

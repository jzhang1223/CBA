from Classes import Query

class CalculationAPI(object):

    CashFlowDB = Query.Query()

    # All calculations with dates take in the date in the datetime format, NOT the SQL string format.

    # Generic function to allow for a specific calculation of the data. Not especially necessary.
    def giveResult(self, result):
        #print result
        # Added for the case of extracting data and getting a 0 result for contributions, distributions, etc
        if result is None:
            return 0
        return result

class CalculationAPI(object):

    # Generic function to allow for a specific calculation of the data.
    def calculate(self, cursor):
        return NotImplementedError("Abstract Class")

import datetime

# Certain formulas used in the model
class ModelCalculations(object):

    # C(t) = RC(t) (CC - PIC(t))
    def contribution(self, rateOfContribution, capitalCommited, paidInCapital):
        return rateOfContribution * (.00 + capitalCommited - paidInCapital)

    # D(t) = RD * [NAV(t-1) * (1 + G)]
    def distribution(self, rateOfDistribution, previousNAV, growthRate):
        return rateOfDistribution * (previousNAV * (1.0 + growthRate))

    # RD = Max[Y, (t / L) ^ B]
    def rateOfDistribution(self, fundYield, year, lifeOfFund, bow):
        print 'Year: ' + str(year)
        print 'Yield: ' + str(fundYield)
        print 'Bow Factor: ' + str(((.00 + year) / lifeOfFund) ** bow)
        return max(fundYield, ((.00 + year) / lifeOfFund) ** (bow))

    # NAV(t) = [NAV(t-1) * (1 + G)] + C(t) - D(t)
    def nav(self, previousNAV, growthRate, contributions, distributions):
        return (previousNAV * (1.0 + growthRate)) + contributions - distributions

    # Solves the following equation to convert an annual contribution percentage into a segmented contribution percentage.
    # initialPercentage + (initialValue * newPercentage) ^ 2 = 1.
    # newPercentage is the variable being solved for.
    # Rounds the percentage to 4 decimal places.
    def segmentCommitment(self, segments, annualPercentage):
        self._checkValidSegments(segments)
        if (segments == 1):
            return annualPercentage
        equation = self._buildEquation(segments)
        return self._binarySolve(equation, annualPercentage)

    # Builds the equation that should be solved based on the number of segments and the initial percentage.
    # Equation is always set equal to 0 to be solved.
    # Used to use n choose k but now uses the pascal row builder.
    def _buildEquation(self, segments):
        self._checkValidSegments(segments)
        equation = []
        pascalRow = self._buildPascalRow(segments)
        for i in range(1, segments + 1):
            # (-1)^(i+1) alternates the negatives, starting with a positive coefficient.
            coefficient = pascalRow[i] * ((-1) ** (i + 1))
            equation.append("{} * {} ** {}".format(coefficient,'{0}', i))
        return " + ".join(equation)

    # Returns an array with the rowNumber of Pascal's triangle.
    # Uses the number to the left to calculate new numbers.
    def _buildPascalRow(self, rowNumber):
        result = [1.0]
        for k in range(rowNumber):
            result.append(result[k] * (rowNumber - k) / (k + 1))
        return result

    # Uses binary search to find the solution to the equation b/c it is known to be between 0 and 1.
    # The equation should not include the annual rate subtracted at the end.
    def _binarySolve(self, equation, annualRate, min=0.0, max=1.0):
        guess = (max - min) / 2.0 + min
        computed = eval(equation.format(guess), None, None)
        if abs(computed - annualRate) < .00001:
            return round(guess, 5)
        elif computed > annualRate:
            return self._binarySolve(equation, annualRate, min, guess)
        else:
            return self._binarySolve(equation, annualRate, guess, max)

    # Returns the annual interest rate split into a number of segments for compounding.
    # The effective interest rate is the given annual interest rate and the nominal rate is being solved for.
    # r = (1+i/n)^n - 1     solve for i => i = n * (nthRoot(1+r) - 1)
    # Does not multiply by segments b/c looking for the actual rate to be used in each month in order to still compound annually.
    def segmentInterest(self, segments, annualPercentage):
        self._checkValidSegments(segments)
        return round((1.0+annualPercentage) ** (1.0/segments) - 1.0, 4)

    # Makes sure that there are a valid number of segments given.
    def _checkValidSegments(self, segments):
        if segments < 1:
            raise ValueError("Invalid Number of Segments")


    # Calculates the remaining commitment for the last year based on a list of previous contributions and the initial capital commitment.
    def commitmentRemaining(self, contributionList, capitalCommitment):
        return .00 + capitalCommitment - sum(contributionList)

    # Calculates the net cash flow for a given year: distribution(t) - contribution(t)
    def netCashFlow(self, contribution, distribution):
        return distribution - contribution

    # Calculates the cummulative cash flow for the last year based on a set of previous cash flows.
    def cummulativeCashFlow(self, cashFlowList):
        return sum(cashFlowList)

    # Returns the calculated end date based on life of the fund and the start date
    def endDate(self, lifeOfFund, startDate):
        endYear = startDate.year + lifeOfFund
        return datetime.date(endYear, startDate.month, startDate.day)

    # Returns the correct date for the given time period and number of segments * original life of fund.
    def correctDate(self, currentTime, startDate, endDate, lifeOfFund):
        dateDifference = endDate - startDate
        scale = (0.0 + currentTime) / lifeOfFund
        return startDate + datetime.timedelta(scale * dateDifference.days)


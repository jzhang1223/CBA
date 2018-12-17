import datetime
from dateutil.relativedelta import relativedelta
from Model import ModelPeriod



# Certain formulas used in the model
class ModelCalculations(object):

    def __init__(self, segments):
        self.modelType = ModelPeriod.ModelPeriod(int(segments))

    # C(t) = RC(t) (CC - PIC(t))
    def contribution(self, rateOfContribution, capitalCommited, paidInCapital):
        return rateOfContribution * (.00 + capitalCommited - paidInCapital)

    # D(t) = RD * [NAV(t-1) * (1 + G)]
    # Also rewritten as RD * [NAV(t-1) + Growth]
    def distribution(self, rateOfDistribution, previousNAV, growthRate, contribution):
        print "giving distribution with: RoD={} PrevNav={} GrowthRate={} Contribution={}".format(rateOfDistribution, previousNAV, growthRate, contribution)

        growth = self.growth(previousNAV, growthRate, contribution)
        print "growth={}".format(growth)
        if self.modelType == ModelPeriod.ModelPeriod.annual:
            return rateOfDistribution * (previousNAV + growth)
        # includes 50% of contributions into growth rate
        elif self.modelType == ModelPeriod.ModelPeriod.quarterly:
            return rateOfDistribution * (previousNAV + growth + contribution)
        else:
            raise NotImplementedError("Models that are not annual or quarterly are currently not supported.")


    # RD = Max[Y, (t / L) ^ B]
    # For non-annual analysis, tries to only use bow factor in last quarter, which will be split up.
    def rateOfDistribution(self, fundYield, year, lifeOfFund, bow):
        print 'Year: ' + str(year)
        print 'Yield: ' + str(fundYield)
        print 'Bow Factor: ' + str(((.00 + year) / lifeOfFund) ** bow)

        return max(fundYield, ((.00 + year) / lifeOfFund) ** bow)

    # NAV(t) = [NAV(t-1) * (1 + G)] + C(t) - D(t)
    # Also rewritten as ... NAV(t) = [NAV(t-1) + Growth] + C(t) - D(t)
    def nav(self, previousNAV, growthRate, contributions, distributions):
        #return (previousNAV * (1.0 + growthRate)) + contributions - distributions
        # includes 50% of contributions of year t into growth
        growth = self.growth(previousNAV, growthRate, contributions)
        print "NAV: prevNav={} growth={} contributions={} distributions={}".format(previousNAV, growth, contributions, distributions)
        return previousNAV + growth + contributions - distributions

    # Growth(t) = [NAV(t-1)] * GrowthRate    ....  for annual model
    # Growth(t) = [NAV(t-1) + .25 * C(t)] * GrowthRate    .... for quarterly model
    def growth(self, previousNAV, growthRate, contributions):
        if self.modelType == ModelPeriod.ModelPeriod.annual:
            return previousNAV * growthRate
        elif self.modelType == ModelPeriod.ModelPeriod.quarterly:
            #return (growthRate * (previousNAV + (contributions * .25)))
            return (previousNAV + (contributions * .25)) * growthRate
        else:
            raise NotImplementedError("Models that are not annual or quarterly are currently not supported.")

    # Solves the following equation to convert an annual contribution percentage into a segmented contribution percentage.
    # initialPercentage + (initialValue * newPercentage) ^ 2 = 1.
    # newPercentage is the variable being solved for.
    # Rounds the percentage to 4 decimal places.
    # NOT CURRENTLY USED, REPLACED WITH expandRates()
    def segmentCommitment(self, segments, annualPercentage):
        self._checkValidSegments(segments)
        if (segments == 1):
            return annualPercentage
        else:
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
            return guess
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
        return (1.0+annualPercentage) ** (1.0/segments) - 1.0

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
    def correctDate(self, currentTime, startDate, segments, lifeOfFund):
        #dateDifference = endDate - startDate
        #scale = (0.0 + currentTime) / lifeOfFund
        #return startDate + datetime.timedelta(scale * dateDifference.days)
        monthDifference = 12.0 / segments
        return startDate + relativedelta(months = monthDifference * currentTime)

    # Returns a growth rate accounting for contribution to generate an equivalent value.
    def _equivalentGrowthRate(self, percentageNeeded, growthRate, principal, contribution):
        growth = principal * (1 + growthRate)
        return (growth * percentageNeeded) / (growth + contribution)

    # Accepts original rates that excludes the 0.0 at the beginning
    def expandRates(self, originalRates, segments, prependZero):
        adjustedRates = []
        if prependZero:
            adjustedRates.append(0.0)
        for rate in originalRates:
            for segment in range(0, segments):
                partialRate = rate / segments
                adjustedRates.append(partialRate / (1.0 - (segment * partialRate)))
        return adjustedRates

    # Given the first date of the fund, number of segments, and years, makes the list of dates for extracting data.
    # **could potentially have issues with ending 0s
    def makeDates(self, firstDate, segments, years):
        pass #todo

#a = ModelCalculations()



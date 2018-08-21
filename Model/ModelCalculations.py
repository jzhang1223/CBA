from sympy.solvers import solve
from sympy import Symbol
from scipy.special import comb

# Certain formulas used in the model
class ModelCalculations(object):

    # C(t) = RC(t) (CC - PIC(t))
    def contribution(self, rateOfContribution, capitalCommited, paidInCapital):
        return rateOfContribution * (.00 + capitalCommited - paidInCapital)

    # D(t) = RD * [NAV(t-1) * (1 + G)]
    def distribution(self, rateOfDistribution, previousNAV, growthRate):
        print rateOfDistribution * (previousNAV * (1.0 + growthRate))
        return rateOfDistribution * (previousNAV * (1.0 + growthRate))

    # RD = Max[Y, (t / L) ^ B]
    def rateOfDistribution(self, fundYield, year, lifeOfFund, bow):
        if (fundYield > ((.00 + year) / lifeOfFund) ** bow):
            print "Using FundYield"
        else:
            print "Using Bow"

        return max(fundYield, ((.00 + year) / lifeOfFund) ** bow)

    # NAV(t) = [NAV(t-1) * (1 + G)] + C(t) - D(t)
    def nav(self, previousNAV, growthRate, contributions, distributions):
        return (previousNAV * (1.0 + growthRate)) + contributions - distributions

    # Solves the following equation to convert an annual contribution percentage into a segmented contribution percentage
    # initialPercentage + (initialValue * newPercentage) ^ 2 = 1
    # newPercentage is the variable being solved for
    # ASSUMES that the answer is the first item of the return in the solve function
    def segmentCommitment(self, segments, initialPercentage):
        equation = self._buildEquation(segments, initialPercentage)
        y = Symbol('y')
        return solve(equation, y)[0]

    # Builds the equation that should be solved based on the number of segments.
    def _buildEquation(self, segments, initialPercentage):
        equation = []
        for i in range(1, segments + 1):
            coefficient = comb(segments, i)
            if i % 2 == 0:
                coefficient *= -1
            equation.append("{} * y ** {}".format(coefficient, i))
        return " + ".join(equation) + " - {}".format(initialPercentage)


    # Not currently used
    def remainingContributions(self, contributionList, capitalCommitment):
        return .00 + capitalCommitment - sum(contributionList)

a = ModelCalculations()
print a._buildEquation(2, .5)
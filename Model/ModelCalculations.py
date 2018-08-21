
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

    # Not currently used
    def remainingContributions(self, contributionList, capitalCommitment):
        return .00 + capitalCommitment - sum(contributionList)
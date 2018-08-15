

class ModelCalculations(object):

    # C(t) = RC(t) (CC – PIC(t))
    def calculateContribution(self, rateOfContribution, capitalCommited, paidInCapital):
        return rateOfContribution * (capitalCommited - paidInCapital)

    # D(t) = RD * [NAV(t-1) * (1 + G)]
    def calculateDistribution(self, rateOfDistribution, previousNAV, growthRate):
        return rateOfDistribution * (previousNAV * (1 + growthRate))

    # RD = Max[Y, (t / L) ^ B]
    def rateOfDistribution(self, fundYield, year, lifeOfFund, bow):
        return max(fundYield, (.00 + year / lifeOfFund) ** bow)

    # NAV(t) = [NAV(t-1) * (1 + G)] + C(t) – D(t)
    def calculateNAV(self, previousNAV, growthRate, contributions, distributions):
        return (previousNAV * (1 + growthRate)) + contributions - distributions

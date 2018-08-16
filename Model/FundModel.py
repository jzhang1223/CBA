import ModelCalculations

# Able to output projected values for a fund based on given information
class FundModel(object):

    def __init__(self, capitalCommitment, contributionRates, bow, growth, fundYield, lifeOfFund):
        """
        Stores the given values for future computations.
        :param capitalCommitment: int of the total capitalCommitment
        :param contributionRates: list of non-empty contribution rates as floats, 50% == 0.5
        :param bow: float of expected bow
        :param growth: float of expected growth
        :param fundYield: float of expected yield
        :param lifeOfFund: int of expected life of the fund in years
        """
        self.capitalCommitment = capitalCommitment
        self.contributionRates = contributionRates
        self.bow = bow
        self.growth = growth
        self.fundYield = fundYield
        self.lifeOfFund = lifeOfFund
        self.calculate = ModelCalculations.ModelCalculations()

    def predictContributions(self):
        result = []
        for i in range(0, self.lifeOfFund):
            realContributionRate = None
            print result
            if len(self.contributionRates) > i:
                print "branch 1"
                realContributionRate = self.contributionRates[i]
            else:
                print "branch 2"
                realContributionRate = self.contributionRates[-1]

            print "rate = " + str(realContributionRate)
            print "comit = " + str(self.capitalCommitment)
            print "remainContr = " + str(self.calculate.remainingContributions(result, self.capitalCommitment))
            result.append(
                self.calculate.contribution(realContributionRate,
                                            self.capitalCommitment,
                                            sum(result)))
            if self.contributionRates[i] > .999999:
                return result
        return result


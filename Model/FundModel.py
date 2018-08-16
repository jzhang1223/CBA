import ModelCalculations

# Able to output projected values for a fund based on given information.
class FundModel(object):

    def __init__(self, capitalCommitment, contributionRates, bow, growthRate, fundYield, lastInvestmentYear, lifeOfFund):
        """
        Stores the given values for future computations.
        :param capitalCommitment: int of the total capitalCommitment
        :param contributionRates: list of non-empty contribution rates as floats, 50% == 0.5
        :param bow: float of expected bow
        :param growthRate: float of expected growth rate
        :param fundYield: float of expected yield
        :param lastInvestmentYear: int of the last year allowed to invest
        """
        self.capitalCommitment = capitalCommitment
        self.contributionRates = contributionRates
        self.bow = bow
        self.growthRate = growthRate
        self.fundYield = fundYield
        self.lastInvestmentYear = lastInvestmentYear
        self.lifeOfFund = lifeOfFund
        self.calculate = ModelCalculations.ModelCalculations()
        self._contributionList = self.predictContributions(0)
        self._distributionList = [0] #todo
        self._navList = [0] #todo

    # Returns the predicted contribution values using the stored fields.
    def predictContributions(self, startingYear):
        result = []

        for i in range(startingYear, self.lastInvestmentYear):
            realContributionRate = None

            if len(self.contributionRates) > i:
                realContributionRate = self.contributionRates[i]
            else:
                realContributionRate = self.contributionRates[-1]

            result.append(
                self.calculate.contribution(realContributionRate,
                                            self.capitalCommitment,
                                            sum(result)))
            if self.contributionRates[i] > .999999:
                break
        return result

    # Predicts the distribution for a given year.
    def predictDistributions(self, currentYear):
        distributionRate = self.calculate.rateOfDistribution(
            self.fundYield, currentYear, self.lastInvestmentYear, self.bow)

        #self._distributionList.append(self.calculate.distribution(
        #    distributionRate, self._navList[currentYear - 1], self.growth))
        return self.calculate.distribution(
            distributionRate, self._navList[currentYear - 1], self.growthRate)

    # Predicts the NAV for a given year.
    def predictNav(self, currentYear):
        print currentYear
        return self.calculate.nav(
            self._navList[currentYear - 1],
            self.growthRate,
            self.getContribution(currentYear),
            self._distributionList[currentYear])

    # Sets the lists of nav and distributions together.
    def setDistributionsAndNav(self, startingYear):
        for i in range(startingYear, self.lifeOfFund):
            self._distributionList.append(self.predictDistributions(i))
            self._navList.append(self.predictNav(i))

    # Gets the contribution of the given year, returning 0 if the year is too high.
    def getContribution(self, year):
        print "year"
        print year
        print "list"
        print len(self._contributionList)
        if year >= len(self._contributionList) :
            return 0
        else:
            return self._contributionList[year]

    def getContributionList(self):
        return self._contributionList

    def getDistributionList(self):
        return self._distributionList

    def getNavList(self):
        return self._navList





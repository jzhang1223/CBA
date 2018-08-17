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
        self._distributionList = [] #todo
        self._navList = [] #todo

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
            self.fundYield, currentYear, self.lifeOfFund, self.bow)

        #self._distributionList.append(self.calculate.distribution(
        #    distributionRate, self._navList[currentYear - 1], self.growth))
        print "printing nav list"
        print self._navList
        print "printing distr list"
        print self._distributionList
        return self.calculate.distribution(
            distributionRate, self.getNav(currentYear - 1), self.growthRate)

    # Predicts the NAV for a given year.
    def predictNav(self, currentYear):
        return self.calculate.nav(
            self.getNav(currentYear - 1),
            self.growthRate,
            self.getContribution(currentYear),
            self.getDistribution(currentYear))

    # Sets the lists of nav and distributions together.
    def setDistributionsAndNav(self, startingYear):
        for i in range(startingYear, self.lifeOfFund):
            print "current year: " + str(i)
            self._distributionList.append(self.predictDistributions(i))
            self._navList.append(self.predictNav(i))

    # Gets the contribution of the given year, returning 0 if the year is too high.
    def getContribution(self, year):
        print "year"
        print year
        print "list"
        print len(self._contributionList)
        if year >= len(self._contributionList):
            return 0
        else:
            return self._contributionList[year]

    def getNav(self, year):
        if year >= len(self._navList) or year < 0:
            return 0
        else:
            return self._navList[year]

    def getDistribution(self, year):
        if year >= len(self._distributionList) or year < 0:
            return 0
        else:
            return self._distributionList[year]

    def getContributionList(self):
        return self._contributionList

    def getDistributionList(self):
        return self._distributionList

    def getNavList(self):
        return self._navList





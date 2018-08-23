import ModelCalculations

# Able to output projected values for a fund based on given information.
class FundModel(object):

    def __init__(self, capitalCommitment, contributionRates, bow, growthRate, fundYield, lastInvestmentYear, lifeOfFund, segments):
        """
        Stores the given values for future computations.
        :param capitalCommitment: int of the total capitalCommitment
        :param contributionRates: list of non-empty contribution rates as floats, 50% == 0.5
        :param bow: float of expected bow
        :param growthRate: float of expected growth rate
        :param fundYield: float of expected yield
        :param lastInvestmentYear: int of the last year allowed to invest
        """
        self.calculate = ModelCalculations.ModelCalculations()
        self.capitalCommitment = capitalCommitment
        #self.contributionRates = contributionRates
        self.bow = bow
        #self.growthRate = growthRate ... compounded
        #self.fundYield = fundYield ... NOT compounded
        #self.lastInvestmentYear = lastInvestmentYear
        #self.lifeOfFund = lifeOfFund

        self._contributionList = []
        self._distributionList = []
        self._navList = []

    # Sets the lists of nav and distributions together.
    def setValues(self):
        for i in range(0, self.lifeOfFund + 1):
            print "current year: " + str(i)
            self._contributionList.append(self.predictContribution(i))
            self._distributionList.append(self.predictDistribution(i))
            self._navList.append(self.predictNav(i))

    # Returns the predicted contribution values using the stored fields.
    def predictContribution(self, currentTime):
        if currentTime > self.lastInvestmentYear or currentTime == 0:
            return 0
        else:
            print "calculating contribution"
            print self.capitalCommitment
            print self.contributionRates[currentTime]
            return self.calculate.contribution(
                self.contributionRates[currentTime - 1],
                self.capitalCommitment,
                sum(self._contributionList))

    # Predicts the distribution for a given year.
    def predictDistribution(self, currentTime):
        if currentTime == 0:
            return 0
        else:
            rateOfDistribution = self.calculate.rateOfDistribution(
                self.fundYield, currentTime, self.lifeOfFund, self.bow)
            return self.calculate.distribution(
                rateOfDistribution, self._navList[currentTime - 1], self.growthRate)

    # Predicts the NAV for a given year.
    def predictNav(self, currentTime):
        if currentTime == 0:
            return self._contributionList[currentTime]
        return self.calculate.nav(self._navList[currentTime - 1],
                                  self.growthRate,
                                  self._contributionList[currentTime],
                                  self._distributionList[currentTime])

    # Sets up the information that changes based on segmenting data.
    def _setupRates(self, segments):
        self.lastInvestmentYear *= segments
        self.lifeOfFund *= segments
        



    '''
    def getContributionList(self):
        return self._contributionList

    def getDistributionList(self):
        return self._distributionList

    def getNavList(self):
        return self._navList
        '''





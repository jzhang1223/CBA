import ModelCalculations

# Able to output projected values for a fund based on given information.
class FundModel(object):

    def __init__(self, capitalCommitment, contributionRates, bow, growthRate, fundYield, lastInvestmentYear, lifeOfFund, segments, startDate):
        """
        Stores the given values for future computations.
        :param capitalCommitment: int of the total capitalCommitment.
        :param contributionRates: list of non-empty contribution rates as floats, 50% == 0.5.
        :param bow: float of expected bow.
        :param growthRate: float of expected growth rate; Converts annual rate to compounded segmented rate.
        :param fundYield: float of expected yield; Converts annual rate to non-compounded segmented rate.
        :param lastInvestmentYear: int of the last year allowed to invest.
        :param segments: int of the number of segments that the model will dive into detail, 1 == annual and 4 == quarterly while other numbers are accepted.
        :param startDate: datetime object which marks the first date of the model.
        """
        self.segments = segments
        self.calculate = ModelCalculations.ModelCalculations()
        self.lastInvestmentYear = lastInvestmentYear * self.segments
        self.lifeOfFund = lifeOfFund * self.segments
        self.capitalCommitment = capitalCommitment
        self.contributionRates = self._expandContributionRates(self.segments, contributionRates)
        self._validateContributionRates(self.contributionRates)
        self.bow = bow
        self.growthRate = self.calculate.segmentInterest(self.segments, growthRate)
        self.fundYield = fundYield / self.segments
        self.startDate = startDate
        self.endDate = self.calculate.endDate(self.lifeOfFund / self.segments, self.startDate)

        self._contributionList = []
        self._distributionList = []
        self._navList = []
        self._commitmentRemainingList = []
        self._netCashFlowList = []
        self._cummulativeCashFlowList = []
        self._dateList = []
        self._setValues()

    # Sets the lists of nav and distributions together.
    def _setValues(self):
        for currentTime in range(self.lifeOfFund + 1):
            self._contributionList.append(round(self.predictContribution(currentTime), 2))
            # commitment remaining
            self._commitmentRemainingList.append(round(self.predictCommitmentRemaining(currentTime), 2))
            self._distributionList.append(round(self.predictDistribution(currentTime), 2))
            # net cash clow
            self._netCashFlowList.append(round(self.predictNetCashFlow(currentTime), 2))
            # cummulative cash flow
            self._cummulativeCashFlowList.append(round(self.predictCummulativeCashFlow(currentTime), 2))
            self._navList.append(round(self.predictNav(currentTime), 2))
            self._dateList.append(self.predictDate(currentTime, self.lifeOfFund))


    # Returns the predicted contribution values based on its own fields.
    def predictContribution(self, currentTime):
        if currentTime > self.lastInvestmentYear or currentTime == 0:
            return 0

        elif currentTime >= len(self.contributionRates):
            contributionRate = self.contributionRates[-1]
        else:
            contributionRate = self.contributionRates[currentTime - 1]

        return self.calculate.contribution(
            contributionRate,
            self.capitalCommitment,
            sum(self._contributionList))

    # Returns the predicted remaining commitment based on previous contributions and the initial commitment.
    #todo tests
    def predictCommitmentRemaining(self, currentTime):
        return self.calculate.commitmentRemaining(self._contributionList, self.capitalCommitment)

    # Predicts the distribution for a given time period based on its own fields.
    def predictDistribution(self, currentTime):
        if currentTime == 0:
            return 0
        else:
            rateOfDistribution = self.calculate.rateOfDistribution(
                self.fundYield, currentTime, self.lifeOfFund, self.bow)
            return self.calculate.distribution(
                rateOfDistribution, self._navList[currentTime - 1], self.growthRate)

    # Predicts the net cash flow for a given time period based on that year's distribution and contributions.
    #todo tests
    def predictNetCashFlow(self, currentTime):
        return self.calculate.netCashFlow(self._contributionList[currentTime], self._distributionList[currentTime])

    # Predicts the cummulative cash flow for a given time period based on the previous cash flows.
    #todo tests
    def predictCummulativeCashFlow(self, currentTime):
        return self.calculate.cummulativeCashFlow(self._netCashFlowList)

    # Predicts the NAV for a given time period based on its own fields.
    def predictNav(self, currentTime):
        if currentTime == 0:
            return self._contributionList[currentTime]
        return self.calculate.nav(self._navList[currentTime - 1],
                                  self.growthRate,
                                  self._contributionList[currentTime],
                                  self._distributionList[currentTime])

    # Expands the contribution rates based on the number of segments and calculating a backtracked rate
    def _expandContributionRates(self, segments, contributionRates):
        result = []
        for originalRate in contributionRates:
            newRate = self.calculate.segmentCommitment(segments, originalRate)
            result.extend([newRate] * segments)
        return result

    # Performs validations on inputted contribution rates.
    def _validateContributionRates(self, contributionRates):
        length = len(contributionRates)
        if length < 1:
            raise ValueError("Can't have 0 contribution rates!")
        for i in range(length):
            temp = contributionRates[i]
            if temp > 1.0 or temp < 0.0:
                raise ValueError("Invalid contribution rate. Make sure it isn't greater than 1 or less than 0")
            elif i != length - 1 and temp == 1.0:
                raise ValueError("Can't have 100% contribution rate not at the end!")

    # Returns the proper date based on the start date, end date, and the lifeOfFund accounting for segments.
    # Uses the start date and end date in the model's fields
    def predictDate(self, currentTime, lifeOfFund):
        return self.calculate.correctDate(currentTime, self.startDate, self.endDate, lifeOfFund)

    '''
    def getContributionList(self):
        return self._contributionList

    def getDistributionList(self):
        return self._distributionList

    def getNavList(self):
        return self._navList
        '''





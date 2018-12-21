from ModelCalculations import ModelCalculations
import pandas as pd
import datetime
from Classes import Extractor
from Calculations import FundStartDate
from Calculations import FundLastDate
from Calculations import ConvertDate
from enum import Enum
from Model import ModelPeriod

# Able to output projected values for a fund based on given information.
# Casts items to their desired types
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
        self.segments = int(segments)
        self.calculate = ModelCalculations(segments)
        if isinstance(startDate, datetime.date):
            self.startDate = startDate
        else:
            dateConverter = ConvertDate.ConvertDate()
            self.startDate = dateConverter(startDate)
        self.endDate = self.calculate.endDate(int(lifeOfFund), self.startDate)
        self.lastInvestmentYear = int(lastInvestmentYear) * self.segments
        self.lifeOfFund = int(lifeOfFund) * self.segments
        self.capitalCommitment = int(capitalCommitment)
        # old code below (before abstraction of rate expansion)
        #self.contributionRates = self._expandContributionRates(self.segments, contributionRates)
        contributionRates = self._appendExtraRates(contributionRates, self.lastInvestmentYear / self.segments)
        self.contributionRates = self.calculate.expandRates(contributionRates, self.segments, False)
        #self._validateContributionRates(self.contributionRates)
        self.bow = float(bow)
        self.growthRate = self.calculate.segmentInterest(self.segments, float(growthRate))#growthRate / self.segments
        self.fundYield = float(fundYield) / self.segments


        self._contributionList = []
        self._distributionList = []
        self._navList = []
        self._commitmentRemainingList = []
        self._netCashFlowList = []
        self._cummulativeCashFlowList = []
        self._dateList = []
        self._typeList = []
        self._distributionRates = []

        self._distributionRates = self.calculate.expandRates(self._getBaseDistributionRates(), self.segments, True)


    # Sets the lists of contributions, distributions, nav, commitment remaining, net cash flow, and cummulative cash flow.
    def forecastValues(self):
        self._setDates(self._getModelLagTime(), self.lifeOfFund + 1)
        # trying new loop and setting the order of contributions
        for currentTime in range(self._getModelTime(), self.lifeOfFund + 1):
            # contributions
            self._contributionList.append(self.predictContribution(currentTime))

        #if (self.segments != 1):
        #    self._swapContributionOrder()

        # Calculates values based on the "current time" of the model, i.e. how much data is already there.
        for currentTime in range(self._getModelTime(), self.lifeOfFund + 1):
            print "_getModelTime() == " + str(self._getModelTime())
            # contributions
            #self._contributionList.append(round(self.predictContribution(currentTime), 2))
            # distributions
            self._distributionList.append(self.predictDistribution(currentTime))
            # nav
            self._navList.append(self.predictNav(currentTime))
            self._typeList.append(EntryType.projection)

        #if (self.segments != 1):
        #    print self._distributionList
        #    self._splitDistributions()


        # Separated in case of partially given data. These values will always be calculated from t = 0.
        # Refactored to be reused when setting actual values, ensuring that the bottom 3 columns are always filled
        self._setBottomThree(self._getModelLagTime(), self.lifeOfFund + 1)

    # Sets actual values for the model
    def setActualValues(self, fund):

        extractor = Extractor.Extractor()
        fundStart = FundStartDate.FundStartDate()
        fundLast = FundLastDate.FundLastDate()

        print "FUND START AND END DATES"
        print fundStart(fund)
        print fundLast(fund)
        extractor.extractActuals(
            fund, fundStart(fund), self.lifeOfFund / self.segments, self.segments, fundLast(fund))
        firstLength = len(extractor.getContributionList())

        if len(extractor.getDistributionList()) != firstLength or len(extractor.getNavList()) != firstLength:
            raise ValueError("Given data must all be the same length!")

        self._setContributionList(extractor.getContributionList())
        self._setDistributionList(extractor.getDistributionList())
        self._setNavList(extractor.getNavList())

        self._setTypeList(0, self._getModelTime(), EntryType.actual)
        self._setBottomThree(0, self._getModelTime())
        self._setDates(0, self._getModelTime())


    # Exports Values to a csv
    def exportToCsv(self, fileName, fundId):

        modelData = self._formatModelToDataframe()
        modelData.insert(loc=0, column="Fund Code", value=[fundId] * 7)
        modelData.insert(loc=1, column="Model Type", value=[self._getModelType().name] * 7)
        modelData.insert(loc=2, column="Model Frequency", value=[self._convertModelPeriod(self.segments)] * 7)
        # 'a' for append
        #todo modify output file
        with open(fileName, 'a') as file:
            print "TRYING TO MOVE TO CSV"
            modelData.to_csv(file, header=True)
            print modelData

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
        return self.calculate.commitmentRemaining(self._contributionList[:currentTime + 1], self.capitalCommitment)

    # Predicts the distribution for a given time period based on its own fields.
    def predictDistribution(self, currentTime):
        if currentTime == 0:
            return 0
        #rateOfDistribution = self.calculate.rateOfDistribution(
        #    self.fundYield, currentTime, self.lifeOfFund, self.bow)
        rateOfDistribution = self._distributionRates[currentTime]
        print "Distribution Parameters: {} {} {}".format(rateOfDistribution, self._navList[currentTime - 1], self.growthRate)
        print "..."
        return self.calculate.distribution(
            rateOfDistribution, self._navList[currentTime - 1], self.growthRate, self._contributionList[currentTime])
        #standard = self.calculate.distribution(
        #    rateOfDistribution, self._navList[currentTime - 1], self.growthRate)

    def _setBottomThree(self, start, stop):
        for segment in range(start, stop):
            # commitment remaining
            self._commitmentRemainingList.append(self.predictCommitmentRemaining(segment))
            # net cash flow
            self._netCashFlowList.append(self.predictNetCashFlow(segment))
            # cummulative cash flow
            self._cummulativeCashFlowList.append(self.predictCummulativeCashFlow(segment))


    # Predicts the net cash flow for a given time period based on that year's distribution and contributions.
    #todo tests
    def predictNetCashFlow(self, currentTime):
        return self.calculate.netCashFlow(self._contributionList[currentTime], self._distributionList[currentTime])

    # Predicts the cummulative cash flow for a given time period based on the previous cash flows.
    #todo tests
    def predictCummulativeCashFlow(self, currentTime):
        return self.calculate.cummulativeCashFlow(self._netCashFlowList[:currentTime + 1])

    # Predicts the NAV for a given time period based on its own fields.
    def predictNav(self, currentTime):
        if currentTime == 0:
            return self._contributionList[currentTime]
        return self.calculate.nav(self._navList[currentTime - 1],
                                  self.growthRate,
                                  self._contributionList[currentTime],
                                  self._distributionList[currentTime])

    # Expands the contribution rates based on the number of segments and calculating a backtracked rate
    #def _expandContributionRates(self, segments, contributionRates):
    #    result = []
    #    for originalRate in contributionRates:
    #        newRate = self.calculate.segmentCommitment(segments, originalRate)
    #        result.extend([newRate] * segments)
    #    return result

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
    def _predictDate(self, currentTime, lifeOfFund):
        return self.calculate.correctDate(currentTime, self.startDate, self.segments, lifeOfFund)

    # Returns the proper ModelPeriod name based on the given number of segments.
    def _convertModelPeriod(self, segments):
        return ModelPeriod.ModelPeriod(segments).name

    # Returns the time of the model based on the number of elements in the list of contributions.
    def _getModelTime(self):
        return len(self._distributionList)

    # Returns the time of the model to start at to "catch up" to fill in the remaining values.
    def _getModelLagTime(self):
        return len(self._commitmentRemainingList)

    # Sets the dates for the fund
    def _setDates(self, start, stop):
        #todo change to using ModelPeriod object or whatever is used for extracting actual data in caluclator class
        for currentTime in range(start, stop):
            self._dateList.append(self._predictDate(currentTime, self.lifeOfFund))

    # Formats the data into a dataframe to be exported
    def _formatModelToDataframe(self):
        return pd.DataFrame(
            [self._dateList, self._contributionList, self._distributionList, self._navList,
             self._commitmentRemainingList, self._cummulativeCashFlowList, self._netCashFlowList],
            index=['Date', 'Contributions', 'Distributions', 'NAV',
                   'Commitment Remaining', 'Cummulative Cash Flow', 'Net Cash Flow'])

    # Reorders the contributions for each year such that, should work for different segments.
    def _swapContributionOrder(self):
        holder = []
        for time in range(1, self.lifeOfFund + 1):
            holder.append(self._contributionList[time])
            if len(holder) == self.segments:
                holder.reverse()
                for i in range((time - self.segments) + 1, time + 1):
                    self._contributionList[i] = holder[(i % self.segments) - 1]
                holder = []

    # Divides the annual distribution into even amounts for each segments.
    def _splitDistributions(self):
        for time in range(0, self.lifeOfFund + 1):
            if self._typeList[time] == EntryType.projection:
                differenceToLastSegment = self._findLastSegmentIndex(time)
                self._distributionList[time] = self._distributionList[time + differenceToLastSegment] / 4
                # Re-adjust the nav after adjusting the distributions. Compounds slightly differently
                self._navList[time] = self.predictNav(time)

    # Determines how many segments away a given time period is.
    def _findLastSegmentIndex(self, time):
        if (time % self.segments == 0):
            return 0
        else:
            return self.segments - (time % self.segments)

    # Sets the corresponding values to actuals or projection types
    def _setTypeList(self, start, stop, type):
        for time in range(start, stop):
            self._typeList.append(type)

    def _getBaseDistributionRates(self):

        #for segment in range(0, self.lifeOfFund + 1):
        #    self._distributionRates.append()
        originalRates = []
        for year in range(1, self.lifeOfFund / self.segments + 1):
            originalRates.append(
                self.calculate.rateOfDistribution(self.fundYield, year, self.lifeOfFund / self.segments, self.bow))

        return originalRates

    # Makes sure that the new contribution rates will be used due to pre-listing contribution rates instead of on the fly calculating
    def _appendExtraRates(self, contributionRates, lastInvestmentYear):
        while len(contributionRates) < lastInvestmentYear:
            print "TESTING"
            print len(contributionRates)
            print lastInvestmentYear
            contributionRates.append(contributionRates[-1])
        return contributionRates

    # Determines whether this is a Model, Actual, or Projection
    def _getModelType(self):
        if EntryType.actual not in self._typeList:
            return ModelType.model
        elif EntryType.projection not in self._typeList:
            return ModelType.actual
        else:
            return ModelType.projection





    '''
    def getContributionList(self):
        return self._contributionList

    def getDistributionList(self):
        return self._distributionList

    def getNavList(self):
        return self._navList
        
        '''

    def _setContributionList(self, newList):
        self._contributionList = newList

    def _setDistributionList(self, newList):
        self._distributionList = newList

    def _setNavList(self, newList):
        self._navList = newList

class EntryType(Enum):
    projection = 0
    actual = 1

class ModelType(Enum):
    model = 0
    actual = 1
    projection = 2
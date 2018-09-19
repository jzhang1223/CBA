from FundModel import FundModel
import pandas as pd
import datetime

def formatModel(fundModel):
    return pd.DataFrame([fundModel._dateList, fundModel._contributionList, fundModel._distributionList, fundModel._navList,
                        fundModel._commitmentRemainingList, fundModel._cummulativeCashFlowList, fundModel._netCashFlowList],
                        index=['Date', 'Contributions', 'Distributions', 'NAV',
                               'Commitment Remaining', 'Cummulative Cash Flow', 'Net Cash Flow'])

pd.set_option('display.expand_frame_repr', False)


commitment1 = 3500000
contributionRates1 = [.4, .66, .67, .4, 1.0]
bow1 = 1.5
growthRate1 = .13
fundYield1 = .06
lastInvestmentYear1 = 4
lifeOfFund1 = 8
segments1 = 1
startDate1 = datetime.date(2008, 3, 20)

fundModel1 = FundModel(commitment1, contributionRates1, bow1, growthRate1,
                                fundYield1, lastInvestmentYear1, lifeOfFund1, segments1, startDate1)
fundModel1.forecastValues()
result1 = formatModel(fundModel1)



segments2 = 4
fundModel2 = FundModel(commitment1, contributionRates1, bow1,
                                 growthRate1, fundYield1, lastInvestmentYear1, lifeOfFund1, segments2, startDate1)
fundModel2.forecastValues()
result2 = formatModel(fundModel2)



contributionRates3 = [.25, 1.0/3, .5]
lastInvestmentYear3 = 8
lifeOfFund3 = 12
bow3 = 2.5
fundYield3 = 0.0
growthRate3 = .13
fundModel3 = FundModel(commitment1, contributionRates3, bow3,
                                 growthRate3, fundYield3, lastInvestmentYear3, lifeOfFund3, segments1, startDate1)
fundModel3.forecastValues()
result3 = formatModel(fundModel3)


print
print result1
print
print result2
print
print result3
print

commitment4 = 5000000
contributionRates4 = [.25, .5, .5, .4, .35]
bow4 = 2.5
growthRate4 = .16
fundYield4 = 0
lastInvestmentYear4 = 6
lifeOfFund4 = 10
segments4 = 1
startDate4 = datetime.date(2015, 1, 1)

actualContribution4 = [0, 1124178, 842202]
actualDistribution4 = [0, 4315, 0]
actualNav4 = [0, 1042235, 2046627]

fundModel4 = FundModel(commitment4, contributionRates4, bow4,
                       growthRate4, fundYield4, lastInvestmentYear4, lifeOfFund4, segments4, startDate4)

fundModel4.setActualValues(actualContribution4, actualDistribution4, actualNav4)
fundModel4.forecastValues()
result4 = formatModel(fundModel4)

# MPPE012015GB
print result4
print


commitment5 = 500000
contributionRates5 = [.25, .33, .5, .25]
bow5 = 2.5
growthRate5 = .15
fundYield5 = 0
lastInvestmentYear5 = 7
lifeOfFund5 = 12
segments5 = 1
startDate5 = datetime.date(2014, 1, 1)

actualContribution5 = [0, 325000, 150000, 10000, 10000]
actualDistribution5 = [0, 0, 21439, 0, 56392]
actualNav5 = [0, 369459, 569448, 588701, 629827]

fundModel5 = FundModel(commitment5, contributionRates5, bow5,
                       growthRate5, fundYield5, lastInvestmentYear5, lifeOfFund5, segments5, startDate5)

fundModel5.setActualValues(actualContribution5, actualDistribution5, actualNav5)
fundModel5.forecastValues()
result5 = formatModel(fundModel5)

#RVVC1A2013MI
print result5
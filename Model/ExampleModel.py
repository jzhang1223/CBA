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
result1 = formatModel(fundModel1)



segments2 = 4
fundModel2 = FundModel(commitment1, contributionRates1, bow1,
                                 growthRate1, fundYield1, lastInvestmentYear1, lifeOfFund1, segments2, startDate1)
result2 = formatModel(fundModel2)



contributionRates3 = [.25, 1.0/3, .5]
lastInvestmentYear3 = 8
lifeOfFund3 = 12
bow3 = 2.5
fundYield3 = 0.0
growthRate3 = .13
fundModel3 = FundModel(commitment1, contributionRates3, bow3,
                                 growthRate3, fundYield3, lastInvestmentYear3, lifeOfFund3, segments1, startDate1)
result3 = formatModel(fundModel3)


print
print result1
print
print result2
print
print result3

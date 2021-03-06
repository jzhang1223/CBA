import pandas as pd
import datetime
from FundModel import FundModel

def formatModel(fundModel):
    return pd.DataFrame([fundModel._dateList, fundModel._contributionList, fundModel._distributionList, fundModel._navList,
                        fundModel._commitmentRemainingList, fundModel._cummulativeCashFlowList, fundModel._netCashFlowList],
                        index=['Date', 'Contributions', 'Distributions', 'NAV',
                               'Commitment Remaining', 'Cummulative Cash Flow', 'Net Cash Flow'])

pd.set_option('display.expand_frame_repr', False)

'''
commitment1 = 1000000
contributionRates1 = [.25, .5, .5, .25]
bow1 = 2.5
growthRate1 = .16
fundYield1 = .0
lastInvestmentYear1 = 6
lifeOfFund1 = 10
segments1 = 4
startDate1 = datetime.date(2014, 12, 31)
'''



commitment1 = 1000000
contributionRates1 = [.3, .6, .5, 1.0]
bow1 = 1.7
growthRate1 = .16
fundYield1 = .0
lastInvestmentYear1 = 5
lifeOfFund1 = 10
segments1 = 1
startDate1 = datetime.date(2014, 12, 31)


'''

commitment1 = 1000000
contributionRates1 = [.4, .6666666666, 1.]
bow1 = 1.7
growthRate1 = .13
fundYield1 = .06
lastInvestmentYear1 = 4
lifeOfFund1 = 8
segments1 = 1
startDate1 = datetime.date(2014, 12, 31)
'''

fundModel1 = FundModel(commitment1, contributionRates1, bow1, growthRate1,
                                fundYield1, lastInvestmentYear1, lifeOfFund1, segments1, startDate1)
#fundModel1.setActualValues('CSPE032015F*')
fundModel1.forecastValues()
result1 = formatModel(fundModel1)
print "RESULT"
print result1
print fundModel1._distributionRates
print fundModel1.contributionRates
print len(fundModel1.contributionRates)

exportFileName = "../../cbaDBdata/RealEstateTemp.csv"
#fundModel1.exportToCsv(exportFileName)

#swapContributionOrder reverted
#rate of distribution only distributing on end year reverted
#split distributions reverted
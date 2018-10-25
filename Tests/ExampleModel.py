from FundModel import FundModel
import pandas as pd
import datetime

def formatModel(fundModel):
    return pd.DataFrame([fundModel._dateList, fundModel._contributionList, fundModel._distributionList, fundModel._navList,
                        fundModel._commitmentRemainingList, fundModel._cummulativeCashFlowList, fundModel._netCashFlowList],
                        index=['Date', 'Contributions', 'Distributions', 'NAV',
                               'Commitment Remaining', 'Cummulative Cash Flow', 'Net Cash Flow'])

pd.set_option('display.expand_frame_repr', False)




exportFileName = "../../cbaDBdata/mp2015.csv" #../../cbaDBdata/testingTemp1.csv"
'''
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




commitment4 = 5000000
contributionRates4 = [.25, .5, .5, .4, .35]
bow4 = 2.5
growthRate4 = .16
fundYield4 = 0
lastInvestmentYear4 = 6
lifeOfFund4 = 10
segments4 = 4
startDate4 = datetime.date(2016, 1, 1)

actualContribution4 = [0, 590964, 40978, 487922, 0, 256267, 537759, 48176, 0, 59507, 698467]
actualDistribution4 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
actualNav4 = [0, 481346, 497637, 1045657, 1042235, 1424458, 1909480, 1943885, 2046627, 2091255, 2916081]

fundModel4 = FundModel(commitment4, contributionRates4, bow4,
                       growthRate4, fundYield4, lastInvestmentYear4, lifeOfFund4, segments4, startDate4)

fundModel4.setActualValues(actualContribution4, actualDistribution4, actualNav4)
fundModel4.forecastValues()
result4 = formatModel(fundModel4)
#fundModel4.exportToCsv(exportFileName)
# MPPE012015GB
'''

commitment4_1 = 5000000
contributionRates4_1 = [.25, .5, .5, .25, .25]
bow4_1 = 2.5
growthRate4_1 = 0.16
fundYield4_1 = 0.0
lastInvestmentYear4_1 = 6
lifeOfFund4_1 = 10
segments4_1 = 1
startDate4_1 = datetime.date(2019, 4, 1)

fundModel4_1 = FundModel(commitment4_1, contributionRates4_1, bow4_1, growthRate4_1,
                         fundYield4_1, lastInvestmentYear4_1, lifeOfFund4_1, segments4_1, startDate4_1)
fundModel4_1.forecastValues()
fundModel4_2 = FundModel(commitment4_1, contributionRates4_1, bow4_1, growthRate4_1,
                         fundYield4_1, lastInvestmentYear4_1, lifeOfFund4_1, 4, startDate4_1)
fundModel4_2.forecastValues()
#fundModel4_3 = FundModel(commitment4_1, contributionRates4_1, bow4_1, growthRate4_1,
#                         fundYield4_1, lastInvestmentYear4_1, lifeOfFund4_1, 12, startDate4_1)
#fundModel4_3.forecastValues()

result4_1 = formatModel(fundModel4_1)
result4_2 = formatModel(fundModel4_2)
#result4_3 = formatModel(fundModel4_3)
# MPPE022018GB

'''
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


commitment6 = 5000000
contributionRates6 = [.4, .66, 1]
bow6 = 1.5
growthRate6 = .13
fundYield6 = .06
lastInvestmentYear6 = 4
lifeOfFund6 = 8
segments6 = 1
startDate6 = datetime.date(2015, 1, 1)

actualContribution6 = [0, 1509678, 715113, 1281598]
actualDistribution6 = [0, 15889, 269404, 545951]
actualNav6 = [0, 1467138, 2204100, 3250219]

fundModel6 = FundModel(commitment6, contributionRates6, bow6,
                       growthRate6, fundYield6, lastInvestmentYear6, lifeOfFund6, segments6, startDate6)

fundModel6.setActualValues(actualContribution6, actualDistribution6, actualNav6)
fundModel6.forecastValues()
result6 = formatModel(fundModel6)

#BSMZ022015GB



commitment7 = 1000000
contributionRates7 = [.25, .33, .5, .25]
bow7 = 2.5
growthRate7 = .15
fundYield7 = .0
lastInvestmentYear7 = 7
lifeOfFund7 = 12
segments7 = 1
startDate7 = datetime.date(2015, 1, 1)

actualContribution7 = [0, 386062, 175000, 155000]
actualDistribution7 = [0, 0, 0, 0]
actualNav7 = [0, 465778, 769025, 915245]

fundModel7 = FundModel(commitment7, contributionRates7, bow7,
                       growthRate7, fundYield7, lastInvestmentYear7, lifeOfFund7, segments7, startDate7)

fundModel7.setActualValues(actualContribution7, actualDistribution7, actualNav7)
fundModel7.forecastValues()
result7 = formatModel(fundModel7)


print
print result1
print
print result2
print
print result3
print
print 'MainPost I'
print result4
print
print 'MainPost II'
print result4_1
print
print result5
print
print result6
print
print result7
print
'''

#print 'MainPost I'
#print result4
print
print 'MainPost II'
print result4_1
print
print result4_2
print
#print result4_3
#fundModel4_1.exportToCsv(exportFileName)
#fundModel4_2.exportToCsv(exportFileName)

print sum(result4_1.loc['Distributions'])
print sum(result4_2.loc['Distributions'])
#print sum(result4_3.loc['Distributions'])



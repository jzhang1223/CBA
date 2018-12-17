from Calculations import CapitalCalled
from Calculations import TotalDistributions
from Calculations import Nav
from dateutil.relativedelta import relativedelta
from Calculations import ConvertDate


# Takes the data from the database to use in the model.
class Extractor(object):

    def __init__(self):
        self.reset()

    # Looks up the actual values and sets its own fields to be them
    def extractActuals(self, fundID, startDate, years, segments, endDate):
        dateList = self._makeDateList(startDate, years, segments, endDate)
        print "PRINTING DATELIST"
        print dateList


        for day in dateList:
            print day
            convertDate = ConvertDate.ConvertDate()
            day = convertDate(day)

            #contribution
            findContribution = CapitalCalled.CapitalCalled()
            print 'Contribution'
            print findContribution(fundID, day)
            print self.contributionList[-1]
            self.contributionList.append(findContribution(fundID, day) - sum(self.contributionList))
            #distribution
            findDistribution = TotalDistributions.TotalDistributions()
            print 'Distribution'
            print findDistribution(fundID, day)
            print self.distributionList[-1]
            self.distributionList.append(findDistribution(fundID, day) - sum(self.distributionList))
            #nav
            findNav = Nav.Nav()
            self.navList.append(findNav(fundID, day))
            print self.navList[-1]

    # Resets the values that are being extracted.
    def reset(self):
        self.contributionList = [0]
        self.distributionList = [0]
        self.navList = [0]

    def getContributionList(self):
        return self.contributionList

    def getDistributionList(self):
        return self.distributionList

    def getNavList(self):
        return self.navList

    # Makes a list of dates starting from the starting date to the end, split based on the number of segments
    def _makeDateList(self, startDate, years, segments, endDate):
        print startDate
        print endDate
        print "Years: {}, Segments: {}".format(years, segments)
        monthDifference = 12.0 / segments
        result = []
        result.append(startDate)
        for period in range(1, years * segments):

            #last date + additional timedifference object
            print result
            nextDate = startDate+relativedelta(months=monthDifference * period)
            #if next date is less than 1 unit of monthDifference between itself and endDate
            if nextDate < endDate or nextDate <= endDate+relativedelta(months=monthDifference):
                result.append(nextDate)
            print "APPEND#{}: {}".format(period, result[-1])

        print result
        return result




e = Extractor()
#print e._makeDateList(datetime.date(10, 7, 21), 5, 4, datetime.date()
#e.extractActuals('RVVC1A2013MI', datetime.date(10, 7, 21), 5, 4)
print e.contributionList
print e.distributionList
#print e.navList
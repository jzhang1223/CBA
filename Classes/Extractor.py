import CapitalCalled
import TotalDistributions
import Nav

# Takes the data from the database to use in the model.
class Extractor(object):

    def __init__(self):
        self.reset()

    def extractActuals(self, fundID, dateList):
        for day in dateList:
            print day

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

e = Extractor()
e.extractActuals('RVVC1A2013MI', ['14/12/31', '15/12/31', '16/12/31', '17/12/31', '18/12/31', '19/12/31'])
print e.contributionList
print e.distributionList
print e.navList
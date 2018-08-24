import unittest
import FundModel

class FundModelTest(unittest.TestCase):

    def reset(self):
        self.commitment1 = 3500000
        self.contributionRates1 = [.4, .66, .67, .4, 1]
        self.bow1 = 1.5
        self.growthRate1 = .13
        self.fundYield1 = .06
        self.lastInvestmentYear1 = 4
        self.lifeOfFund1 = 8
        self.segments1 = 1
        self.fundModel = FundModel.FundModel(self.commitment1, self.contributionRates1, self.bow1,
            self.growthRate1, self.fundYield1, self.lastInvestmentYear1, self.lifeOfFund1, self.segments1)

    # Testing contributions
    def test_1_simple(self):
        self.reset()
        # 22 CCDD062016AF	2016	 $3,500,000 	12/31/17	40%	66%	67%	40%	100%    1.50 	13%	6%
        #  $1,400,000 	 $1,386,000 	 $476,000 	 $95,200   ... remaining  141372.0
        self.assertEqual([1400000.0, 1386000.0, 478380.0, 94248.0], self.fundModel.setValues(0))

        self.assertEqual(len(self.fundModel._distributionList), 1)
        self.assertEqual(len(self.fundModel._navList), 1)

    # Testing distributions and navs
    def test_2_simple(self):
        self.reset()
        self.fundModel.setValues()
        print self.fundModel._contributionList
        print self.fundModel._distributionList
        print self.fundModel._navList
        #  $84,000 	 $185,885 	 $697,308 	 $1,124,725 	 $1,201,367 	 $902,787 	 $450,556 	 $112,907
        self.assertEqual([84000.0, 185885.0, 697308.0, 1124725.0, 1201367.0, 902787.0, 450556.0, 112907.0],
                         self.fundModel._distributionList)
        #  $1,316,000 	 $2,687,195 	 $2,815,223 	 $2,151,677 	 $1,230,028 	 $487,145 	 $99,918

    def test_3_expandContributionRates(self):
        self.reset()
        segments = 2
        rates = [.5, .7]
        result = [.29289, .29289, .45227, .45227]
        self.assertEqual(result, self.fundModel._expandContributionRates(segments, rates))

    def test_4_expandContributionRates(self):
        self.reset()
        segments = 4
        rates = [.4, .5]
        result = [.11989, .11989 ,.11989 ,.11989, .1591, .1591, .1591, .1591]
        self.assertEqual(result, self.fundModel._expandContributionRates(segments, rates))

    def test_5_example(self):
        self.reset()
        self.segments1 = 4
        self.fundModel = FundModel.FundModel(self.commitment1, self.contributionRates1, self.bow1,
            self.growthRate1, self.fundYield1, self.lastInvestmentYear1, self.lifeOfFund1, self.segments1)
        self.fundModel.setValues()
        print self.fundModel._contributionList
        print self.fundModel._distributionList
        print self.fundModel._navList
        #  $84,000 	 $185,885 	 $697,308 	 $1,124,725 	 $1,201,367 	 $902,787 	 $450,556 	 $112,907
        #self.assertEqual([84000.0, 185885.0, 697308.0, 1124725.0, 1201367.0, 902787.0, 450556.0, 112907.0],
        #                 self.fundModel._distributionList)
import unittest
import FundModel

class FundModelTest(unittest.TestCase):

    def reset(self):
        self.commitment1 = 3500000
        self.contributionRates1 = [.4, .66, .67, .4, 1.0]
        self.bow1 = 1.5
        self.growthRate1 = .13
        self.fundYield1 = .06
        self.lastInvestmentYear1 = 4
        self.lifeOfFund1 = 8
        self.segments1 = 1
        self.fundModel = FundModel.FundModel(self.commitment1, self.contributionRates1, self.bow1, self.growthRate1,
                                             self.fundYield1, self.lastInvestmentYear1, self.lifeOfFund1, self.segments1)

    # Testing contributions
    def test_1_simple(self):
        self.reset()
        # 22 CCDD062016AF	2016	 $3,500,000 	12/31/17	40%	66%	67%	40%	100%    1.50 	13%	6%
        #  $1,400,000 	 $1,386,000 	 $476,000 	 $95,200   ... remaining  141372.0
        print self.fundModel._contributionList
        print self.fundModel._distributionList
        print self.fundModel._navList
        self.assertEqual([0.0, 1400000.0, 1386000.0, 478380.0, 94248.0, 0.0, 0.0, 0.0, 0.0], self.fundModel._contributionList)


    # Testing contributions, distributions, and navs for a standard model.
    def test_2_simple(self):
        self.reset()
        print self.fundModel._contributionList
        print self.fundModel._distributionList
        print self.fundModel._navList
        # Contributions: $0  $1400000  $1386000  $478380  $94248  $0  $0  $0  $0
        # Distributions: $0  $0  $197750  $718859.9836  $1154560.361  $1231293.856  $925276.7571  $461779.5483  $115719.7454
        # Nav: $0  $1400000  $2770250  $2889902.516  $2205277.482  $1260669.699  $499280.0023  $102406.8543  $0

        self.assertEqual([0.0, 1400000.0, 1386000.0, 478380.0, 94248.0, 0.0, 0.0, 0.0, 0.0],
                         self.fundModel._contributionList)
        self.assertEqual([0.0, 0.0, 197750.0, 718859.98, 1154560.36, 1231293.86, 925276.76, 461779.55, 115719.74],
                         self.fundModel._distributionList)
        self.assertEqual([0.0, 1400000.0, 2770250.0, 2889902.52, 2205277.49, 1260669.70, 499280.00, 102406.85, 0.0],
                         self.fundModel._navList)

    # Testing using the last contribution until the end.
    def test_2_1_simple(self):

        self.reset()
        self.contributionRates1 = [.25, 1.0/3, .5]
        self.lastInvestmentYear1 = 8
        self.lifeOfFund1 = 12
        self.bow1 = 2.5
        self.fundYield1 = 0.0
        self.growthRate1 = .13
        self.fundModel = FundModel.FundModel(self.commitment1, self.contributionRates1, self.bow1, self.growthRate1,
                                             self.fundYield1, self.lastInvestmentYear1, self.lifeOfFund1, self.segments1)
        print self.fundModel._contributionList
        print self.fundModel._distributionList
        print self.fundModel._navList

        self.assertEqual([0.0, 875000.0, 875000.0, 875000.0, 437500.0, 218750.0, 109375.0, 54687.5, 27343.75, 0.0, 0.0, 0.0, 0.0],
                         self.fundModel._contributionList)
        self.assertEqual([0.0, 0.0, 11212.65, 65417.73, 210433.45, 444156.04, 746685.24, 1053297.05, 1252423.86, 1225447.34, 924200.61, 485155.42, 133219.26],
                         self.fundModel._distributionList)
        self.assertEqual([0.0, 875000.0, 1852537.35, 2902949.48, 3507399.46, 3737955.35, 3586579.31, 3054225.07, 2226194.22, 1290152.13, 533671.3, 117893.15, 0.0],
                         self.fundModel._navList)


    # Tests contribution rates split into halves
    def test_3_expandContributionRates(self):
        self.reset()
        self.segments1 = 2
        rates = [.5, .7]
        result = [.29289, .29289, .45227, .45227]
        self.assertEqual(result, self.fundModel._expandContributionRates(self.segments1, rates))

    # Tests contribution rates split into quarters.
    def test_4_expandContributionRates(self):
        self.reset()
        self.segments1 = 4
        rates = [.4, .5]
        result = [.11989, .11989 ,.11989 ,.11989, .1591, .1591, .1591, .1591]
        self.assertEqual(result, self.fundModel._expandContributionRates(self.segments1, rates))

    # Tests splitting rates into 1 segment, ie should return the same list
    def test_4_1_expandContributionRates(self):
        self.reset()
        rates = [.2, .5, .9, 1]
        self.assertEqual(rates, self.fundModel._expandContributionRates(self.segments1, rates))

    # Tests splitting a list of rates that has a 1 in it into multiple parts.
    def test_4_2_expandContributionRates(self):
        self.reset()
        rates = [.25, .5, 1]
        self.assertEqual(None, self.fundModel._expandContributionRates(3, rates))

    # Tests a model segmented into quarters.
    # todo
    def test_5_example(self):
        self.reset()
        self.segments1 = 4
        self.fundModel = FundModel.FundModel(self.commitment1, self.contributionRates1, self.bow1,
            self.growthRate1, self.fundYield1, self.lastInvestmentYear1, self.lifeOfFund1, self.segments1)

        print self.fundModel._contributionList
        print self.fundModel._distributionList
        print self.fundModel._navList
        print self.fundModel._expandContributionRates(2, [1])
        #  $84,000 	 $185,885 	 $697,308 	 $1,124,725 	 $1,201,367 	 $902,787 	 $450,556 	 $112,907
        #self.assertEqual([84000.0, 185885.0, 697308.0, 1124725.0, 1201367.0, 902787.0, 450556.0, 112907.0],
        #                 self.fundModel._distributionList)

    # Tests validating contribution rates, making sure error is raised correctly when a 1 is in the middle.
    def test_6_validateContributionRates(self):
        self.reset()
        with self.assertRaises(ValueError):
            self.contributionRates1 = [.3, 1.0, .4]
            self.fundModel = FundModel.FundModel(self.commitment1, self.contributionRates1, self.bow1,
                                                 self.growthRate1, self.fundYield1, self.lastInvestmentYear1,
                                                 self.lifeOfFund1, self.segments1)

    # Tests validating contribution rates, making sure error is raised correctly when a value > 1 is in.
    def test_7_validateContributionRates(self):
        self.reset()
        with self.assertRaises(ValueError):
            self.contributionRates1 = [.3, .5, 1.3, .4]
            self.fundModel = FundModel.FundModel(self.commitment1, self.contributionRates1, self.bow1,
                                                 self.growthRate1, self.fundYield1, self.lastInvestmentYear1,
                                                 self.lifeOfFund1, self.segments1)

    # Tests validating contribution rates, making sure error is raised correctly when a value > 1 is at end.
    def test_8_validateContributionRates(self):
        self.reset()
        with self.assertRaises(ValueError):
            self.contributionRates1 = [.3, .5, .2, 1.4]
            self.fundModel = FundModel.FundModel(self.commitment1, self.contributionRates1, self.bow1,
                                                 self.growthRate1, self.fundYield1, self.lastInvestmentYear1,
                                                 self.lifeOfFund1, self.segments1)

    # Tests validating contribution rates, making sure error is raised correctly when a value < 0 is in.
    def test_9_validateContributionRates(self):
        self.reset()
        with self.assertRaises(ValueError):
            self.contributionRates1 = [.3, -.1, .4, .4]
            self.fundModel = FundModel.FundModel(self.commitment1, self.contributionRates1, self.bow1,
                                                 self.growthRate1, self.fundYield1, self.lastInvestmentYear1,
                                                 self.lifeOfFund1, self.segments1)

    # Tests validating contribution rates, making sure error is raised correctly when length < 1
    def test_10_validateContributionRates(self):
        self.reset()
        with self.assertRaises(ValueError):
            self.contributionRates1 = []
            self.fundModel = FundModel.FundModel(self.commitment1, self.contributionRates1, self.bow1,
                                                 self.growthRate1, self.fundYield1, self.lastInvestmentYear1,
                                                 self.lifeOfFund1, self.segments1)

    # Tests that net cash flow is correct by comparing to the total sum of contributions and distributions.
    def test_11_checkNetCashFlow(self):
        self.reset()
        self.assertEqual(round(sum(self.fundModel._netCashFlowList), 2),
                         sum(self.fundModel._distributionList) - sum(self.fundModel._contributionList))

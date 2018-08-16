import unittest
import FundModel


class FundModelTest(unittest.TestCase):



    def test_simple(self):
        # 22 CCDD062016AF	2016	 $3,500,000 	12/31/17	40%	66%	67%	40%	100%    1.50 	13%	6%
        commitment1 = 3500000
        contributionRates1 = [.4, .66, .67, .4, 1]
        bow1 = 1.5
        growth1 = .13
        fundYield1 = .06
        lifeOfFund1 = 8
        fundModel = FundModel.FundModel(commitment1, contributionRates1, bow1, growth1, fundYield1, lifeOfFund1)

        #  $1,400,000 	 $1,386,000 	 $476,000 	 $95,200
        self.assertEqual([1400000.0, 1386000.0, 478380.0, 94248.0, 141372.0], fundModel.predictContributions())
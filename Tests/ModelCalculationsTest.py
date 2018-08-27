import ModelCalculations
import unittest

class ModelCalculationsTest(unittest.TestCase):

    # 2 Segments: x = 2y - y^2
    # 3 Segments: x = 3y - 3y^2 + y^3
    # 4 Segments: x = 4y - 6y^2 + 4y^3 - y^4
    # 5 Segments: x = 5y - 10y^2 + 10y^3 - 5y^4 + y^5

    def reset(self):
        self.calculator = ModelCalculations.ModelCalculations()

    # 2 segments, initially .5 contribution
    def test_1_buildEquation(self):
        self.reset()
        self.assertEqual("2.0 * {0} ** 1 + -1.0 * {0} ** 2", self.calculator._buildEquation(2))

    # 4 segments, initially .4 contribution
    def test_2_buildEquation(self):
        self.reset()
        self.assertEqual("4.0 * {0} ** 1 + -6.0 * {0} ** 2 + 4.0 * {0} ** 3 + -1.0 * {0} ** 4", self.calculator._buildEquation(4))

    # 1 segment, initially .7 contribution
    def test_3_buildEquation(self):
        self.reset()
        self.assertEqual("1.0 * {0} ** 1", self.calculator._buildEquation(1))

    # 2 segments, initially .5 contribution
    def test_4_segmentContribution(self):
        self.reset()
        self.assertEqual(.29289, self.calculator.segmentCommitment(2, .5))

    # 1 segment, initially .7 contribution
    def test_5_segmentContribution(self):
        self.reset()
        self.assertEqual(.7, self.calculator.segmentCommitment(1, .7))

    # Another added test
    def test_5_1_segmentContribtuion(self):
        self.reset()
        self.assertEqual(.45227, self.calculator.segmentCommitment(2, .7))

    # Added a year = 0 test
    def test_5_2_segmentContribution(self):
        self.reset()
        with self.assertRaises(ValueError):
            self.calculator.segmentCommitment(0, .4)

    # Added a year = 1 test
    def test_5_3_segmentContribution(self):
        self.reset()
        self.assertEqual(.9, self.calculator.segmentCommitment(1, .9))

    #4 segments, initially .4 contribution
    def test_6_segmentContribution(self):
        self.reset()
        self.assertEqual(.11989, self.calculator.segmentCommitment(4, .4))

    def test_7_reductionMatches(self):
        self.reset()
        value = 100
        initialPercentage = .3
        # Max segments = 103
        segments = 103
        newPercentage = self.calculator.segmentCommitment(segments, initialPercentage)
        for i in range(0, segments):
            value -= value * newPercentage
        self.assertEqual(70.0, round(value, 1))

    # Row number 5 (0 indexing) of Pascal's triangle
    def test_8_buildPascalRow(self):
        self.reset()
        rowNumber = 5
        self.assertEqual([1, 5, 10, 10, 5, 1], self.calculator._buildPascalRow(rowNumber))

    # Based on investopedia 10% data for semiannual, quarterly, monthly, daily
    # Checks that given a compounded interest rate split into n segments should always go back to .1
    def test_9_segmentInterest(self):
        self.reset()
        dict = {1:.1, 2:.1025, 4:.10381, 12:.10471, 365:.10516}
        for i in dict:
            self.assertEqual(.1, self.calculator.segmentInterest(i, dict[i]))

    # Same as test_9 except more diversified values.
    def test_10_segmentInterest(self):
        self.reset()
        result = ((12,.16076,.15), (4,.21551,.2), (52,.07246,.07))
        for i in result:
            print i[0]
            print i[1]
            print i[2]
            self.assertEqual(i[2], self.calculator.segmentInterest(i[0], i[1]))


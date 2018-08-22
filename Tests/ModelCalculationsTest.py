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
        self.assertEqual("2.0 * y ** 1 + -1.0 * y ** 2 - 0.5", self.calculator._buildEquation(2, .5))

    # 4 segments, initially .4 contribution
    def test_2_buildEquation(self):
        self.reset()
        self.assertEqual("4.0 * y ** 1 + -6.0 * y ** 2 + 4.0 * y ** 3 + -1.0 * y ** 4 - 0.4", self.calculator._buildEquation(4, .4))

    # 1 segment, initially .7 contribution
    def test_3_buildEquation(self):
        self.reset()
        self.assertEqual("1.0 * y ** 1 - 0.7", self.calculator._buildEquation(1, .7))

    # 2 segments, initially .5 contribution
    def test_4_segmentContribution(self):
        self.reset()
        self.assertEqual(.2929, self.calculator.segmentCommitment(2, .5))

    # 1 segment, initially .7 contribution
    def test_5_segmentContribution(self):
        self.reset()
        self.assertEqual(.7, self.calculator.segmentCommitment(1, .7))

    #4 segments, initially .4 contribution
    def test_6_segmentContribution(self):
        self.reset()
        self.assertEqual(.1199, self.calculator.segmentCommitment(4, .4))

    def test_7_reductionMatches(self):
        # 6 ~ 1s
        # 9 ~ 34s
        # 10 ~ 47s
        # 11 ~ 63s
        self.reset()
        value = 100
        initialPercentage = .3
        segments = 1
        newPercentage = self.calculator.segmentCommitment(segments, initialPercentage)
        for i in range(0, segments):
            print i
            value -= value * newPercentage
        self.assertEqual(70.0, round(value, 1))


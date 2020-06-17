"""Testing file comprising Frequentist & Bayesian A/B Testing methods."""

import unittest
from pyab.experiments import ABTestFrequentist, ABTestBayesian

class TestClass(unittest.TestCase):
    """
    A/B Testing unittest Class.
    """

    def test_t_test(self):
        exp_freq = ABTestFrequentist()
        exp_freq.conduct_experiment(1,10,2,10)
        self.assertEqual(True, exp_freq.is_t_test)

    def test_norm_test(self):
        exp_freq = ABTestFrequentist()
        exp_freq.conduct_experiment(1,100,2,100)
        self.assertEqual(False, exp_freq.is_t_test)

    def test_one_tailed(self):
        exp = ABTestFrequentist(alpha=0.05, alt_hypothesis='one_tailed')
        stat, pvalue = exp.conduct_experiment(100,1000,125,1000)

        self.assertAlmostEqual(stat, 1.77, 2)
        self.assertAlmostEqual(pvalue, 0.038, 2)

    def test_two_tailed(self):
        exp = ABTestFrequentist(alpha=0.05, alt_hypothesis='two_tailed')
        stat, pvalue = exp.conduct_experiment(100,1000,125,1000)

        self.assertAlmostEqual(stat, 1.77, 2)
        self.assertAlmostEqual(pvalue, 0.077, 2)

    def test_power(self):
        exp = ABTestFrequentist(alpha=0.05, alt_hypothesis='two_tailed')
        exp.conduct_experiment(100,1000,125,1000)

        self.assertAlmostEqual(1-exp.beta, 0.424372, 2)

if __name__ == '__main__':
    unittest.main()
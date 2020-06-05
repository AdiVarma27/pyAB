"""Main file comprising Frequentist & Bayesian A/B Testing methods."""


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st
import statsmodels.stats.api as sms
from statsmodels.stats.power import tt_ind_solve_power
from pyab.utils import check_data_input, check_t_test


class ABTestFrequentist:
    """
    Frequentist A/B Testing aka Two sample proportion test.

    Parameters
    ----------
    alpha : float, default = 0.05
        Significane level or Type 1 error rate.

    alt_hypothesis : str, default = 'one_tailed'
        One or two tailed hypothesis test.

        * 'one_tailed':
            one tailed hypothesis test
        * 'two_tailed':
            two tailed hypothesis test
    """

    def __init__(self, alpha=0.05, alt_hypothesis='one_tailed'):

        self.alpha = alpha

        self.alt_hypothesis = alt_hypothesis
        self.stat = None
        self.stat_null_crit_upper = None
        self.stat_null_crit_lower = None

        all_alt_hypothesis = ['one_tailed', 'two_tailed']
        if alt_hypothesis not in all_alt_hypothesis:
            raise ValueError(
                "ABTestFrequentist class supports hypothesis in %s, got %s"
                % (all_alt_hypothesis, alt_hypothesis)
            )

    def calculate_power(self, stat):
        """
        Calculate power (1-beta) at given test statistics.

        Parameters
        ----------
        stat : float
            z or t test statistic.

        Returns
        -------
        1 - beta : float
            power at given test statistic.
        """
        dist_alt = st.norm(loc=stat)
        if self.right_tailed_flag:
            beta = dist_alt.cdf(self.stat_null_crit_upper)
        else:
            beta = 1 - dist_alt.cdf(self.stat_null_crit_lower)

        return 1 - beta

    def calculate_stat(self, prop_alt):
        """
        Calculate test statistic with current experiment parameters.

        Parameters
        ----------
        prop_alt : float
            alternate hypothesis proportion.

        Returns
        -------
        stat : float
            z or t statistic.
        """
        diff_prop = prop_alt - self.prop_null

        self.right_tailed_flag = True if diff_prop >= 0 else False

        moving_success_alt = prop_alt * self.trials_alt

        prop_pooled = (self.success_null + moving_success_alt) / (
            self.trials_null + self.trials_alt
        )

        variance = (
            (prop_pooled) * (1 - prop_pooled)
            * ((1 / self.trials_null) + (1 / self.trials_alt))
        )

        stat = diff_prop / np.sqrt(variance)

        return stat

    def conduct_experiment(self, success_null, trials_null, success_alt, trials_alt):
        """
        Conduct experiment & generate power curve with provided parameters.

        Parameters
        ----------
        success_null : int
            number of successful clicks or successful events (Version-A).

        trials_null : int
            number of impressions or events (Version-A)

        success_alt : int
            number of successful clicks or successful events (Version-B).

        trials_alt : int
            number of impressions or events (Version-B).

        Returns
        -------
        stat : float
            z or t statistic.

        pvalue : float
            probability of obtaining results atleast as extreme as the results actually observed during the test.
        """
        check_data_input(success_null, trials_null)
        check_data_input(success_alt, trials_alt)

        self.success_null = success_null
        self.trials_null = trials_null
        self.prop_null = success_null / trials_null
        self.success_alt = success_alt
        self.trials_alt = trials_alt
        self.prop_alt = success_alt / trials_alt

        self.stat = self.calculate_stat(self.prop_alt)

        self.is_t_test = True if check_t_test(trials_null, trials_alt) else False

        # check for alt hypothesis
        if self.alt_hypothesis == 'one_tailed':

            # check if t-test
            if self.is_t_test:
                if self.right_tailed_flag:
                    self.pvalue = st.t.cdf(-self.stat,
                                      df=trials_null + trials_alt - 2)
                else:
                    self.pvalue = st.t.cdf(
                        self.stat, df=trials_null + trials_alt - 2)

                self.stat_null_crit_lower = st.t.ppf(self.alpha)
                self.stat_null_crit_upper = st.t.ppf(1 - self.alpha)

            # if not t-test
            else:
                if self.right_tailed_flag:
                    self.pvalue = st.norm.cdf(-self.stat)
                else:
                    self.pvalue = st.norm.cdf(self.stat)

                self.stat_null_crit_lower = st.norm.ppf(self.alpha)
                self.stat_null_crit_upper = st.norm.ppf(1 - self.alpha)

            self.conf_int_null_crit = (
                self.prop_null + self.stat_null_crit_lower
                * np.sqrt(self.prop_null * (1 - self.prop_null)
                          * (1 / trials_null)),
                self.prop_null
                + self.stat_null_crit_upper
                * np.sqrt(self.prop_null * (1 - self.prop_null)
                          * (1 / trials_null))
            )

            self.beta = 1 - self.calculate_power(self.stat)

            if self.right_tailed_flag:
                self.power_curve = {
                    temp_moving_prop: self.calculate_power(
                        self.calculate_stat(temp_moving_prop)
                    )
                    for temp_moving_prop in np.arange(self.prop_null, 1.005, 0.005)
                }

            else:
                self.power_curve = {
                    temp_moving_prop: self.calculate_power(
                        self.calculate_stat(temp_moving_prop)
                    )
                    for temp_moving_prop in np.arange(0, self.prop_null + 0.005, 0.005)
                }

        # if two-tailed
        else:
            # check if t-test
            if self.is_t_test:
                if self.right_tailed_flag:
                    self.pvalue = st.t.cdf(-self.stat,
                                      df=trials_null + trials_alt - 2) * 2
                else:
                    self.pvalue = st.t.cdf(
                        self.stat, df=trials_null + trials_alt - 2) * 2

                self.stat_null_crit_lower = st.t.ppf(self.alpha / 2)
                self.stat_null_crit_upper = st.t.ppf(1 - self.alpha / 2)

            # if not t-test
            else:
                if self.right_tailed_flag:
                    self.pvalue = st.norm.cdf(-self.stat) * 2
                else:
                    self.pvalue = st.norm.cdf(self.stat) * 2

                self.stat_null_crit_lower = st.norm.ppf(self.alpha / 2)
                self.stat_null_crit_upper = st.norm.ppf(1 - self.alpha / 2)

            # calculate conf int
            self.conf_int_null_crit = (
                self.prop_null + self.stat_null_crit_lower * np.sqrt(self.prop_null * (1 - self.prop_null) * (1 / trials_null)),
                self.prop_null + self.stat_null_crit_upper * np.sqrt(self.prop_null * (1 - self.prop_null) * (1 / trials_null)),
            )

            self.beta = 1 - self.calculate_power(self.stat)

            if self.right_tailed_flag:
                self.power_curve = {
                    temp_moving_prop: self.calculate_power(
                        self.calculate_stat(temp_moving_prop)
                    )
                    for temp_moving_prop in np.arange(0, 1.005, 0.005)
                }

            else:
                self.power_curve = {
                    temp_moving_prop: self.calculate_power(
                        self.calculate_stat(temp_moving_prop)
                    )
                    for temp_moving_prop in np.arange(0, 1.005, 0.005)
                }

        self.print_freq_results()

        return self.stat, self.pvalue

    def get_sample_size(self, beta=0.1):
        """
        Calculate required sample size per group to obtain provided beta.

        Parameters
        ----------
        beta : float
            Type 2 error rate.

        Returns
        -------
        n : float
            sample size per group.
        """
        es = sms.proportion_effectsize(self.prop_null, self.prop_alt)

        if self.alt_hypothesis == 'two_tailed':
            n = tt_ind_solve_power(
                effect_size=es,
                alpha=self.alpha,
                power=1 - beta,
                alternative='two-sided',
            )
        else:
            n = tt_ind_solve_power(
                effect_size=es, alpha=self.alpha, power=1 - beta, alternative='smaller'
            )

        return n

    def print_freq_results(self):
        """
        Print Frequentist Experiment Results
        """
        is_significant = False

        if self.pvalue < self.alpha:
            is_significant = True

        print("pyAB Summary\n============\n")
        print("Test Parameters\n_______________\n")
        print("Variant A: Success Rate %s, Sample Size %s" %(self.prop_null, self.trials_null))
        print("Variant B: Success Rate %s, Sample Size %s" %(self.prop_alt, self.trials_alt))
        print("Type-I Error: %s, %s test\n" %(self.alpha, self.alt_hypothesis))
        print("Test Results\n____________\n")
        if is_significant:
            print("There is a statistically significant difference in proportions of two variants\n")
        else:
            print("There is no statistically significant difference in proportions of two variants\n")
        print("Test Stat: %s" % (np.round(self.stat, 3)))
        print("p-value: %s" % (np.round(self.pvalue, 3)))
        print("Type-II Error: %s" % (np.round(self.beta, 3)))

    def plot_power_curve(self, figsize=(9, 6)):
        """
        Plot power curve for provided experiment parameters.

        Parameters
        ----------
        figsize : tuple, default = (12,8)
            matplotlib plot size.
        """
        power_curve_ind, power_curve_values = (
            np.array(list(self.power_curve.keys())),
            np.array(list(self.power_curve.values())),
        )

        power_curve_diff = np.abs(np.diff(power_curve_values))

        power_curve_cutoff = 1.0e-5

        plot_power_curve_ind = np.where(
            power_curve_diff > power_curve_cutoff)[0]

        plot_power_curve_values = power_curve_values[plot_power_curve_ind]

        plot_power_curve_proportion = power_curve_ind[plot_power_curve_ind]

        plt.figure(figsize=figsize)
        sns.lineplot(plot_power_curve_proportion, plot_power_curve_values)
        plt.scatter(self.prop_alt, 1 - self.beta)
        plt.xlabel("Comparison Proportion")
        plt.ylabel("Power")
        plt.grid()
        plt.plot()

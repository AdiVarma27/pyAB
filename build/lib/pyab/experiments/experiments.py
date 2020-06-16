"""Main file comprising Frequentist & Bayesian A/B Testing methods."""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as st
import statsmodels.stats.api as sms
from statsmodels.stats.power import tt_ind_solve_power
from pyab.utils import check_valid_input, check_valid_parameter, check_t_test

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

        check_valid_parameter(alpha)

        if alt_hypothesis not in all_alt_hypothesis:
            raise ValueError(
                "ABTestFrequentist class supports hypothesis in %s, got %s"
                % (all_alt_hypothesis, alt_hypothesis)
            )

    def conduct_experiment(self, success_null, trials_null, success_alt, trials_alt):
        """
        Conduct experiment & generate power curve with provided parameters.

        Parameters
        ----------
        success_null : int
            number of successful clicks or successful events (Version-A).

        trials_null : int
            number of impressions or events (Version-A).

        success_alt : int
            number of successful clicks or successful events (Version-B).

        trials_alt : int
            number of impressions or events (Version-B).

        Returns
        -------
        stat : float
            z or t statistic.

        pvalue : float
            probability of obtaining results atleast as extreme as the results
            actually observed during the test.
        """

        check_valid_input(success_null, trials_null)
        check_valid_input(success_alt, trials_alt)

        self.success_null = success_null
        self.trials_null = trials_null
        self.prop_null = success_null / trials_null
        self.success_alt = success_alt
        self.trials_alt = trials_alt
        self.prop_alt = success_alt / trials_alt

        self.stat = self.calculate_stat(self.prop_alt)
        self.is_t_test = True if check_t_test(
            trials_null, trials_alt) else False

        if self.alt_hypothesis == 'one_tailed':
            if self.is_t_test:
                if self.right_tailed_flag:
                    self.pvalue = st.t.cdf(-self.stat,
                                           df=trials_null + trials_alt - 2)
                else:
                    self.pvalue = st.t.cdf(
                        self.stat, df=trials_null + trials_alt - 2)

                self.stat_null_crit_lower = st.t.ppf(
                    self.alpha, df=trials_null + trials_alt - 2)

                self.stat_null_crit_upper = st.t.ppf(
                    1 - self.alpha, df=trials_null + trials_alt - 2)

            else:
                if self.right_tailed_flag:
                    self.pvalue = st.norm.cdf(-self.stat)
                else:
                    self.pvalue = st.norm.cdf(self.stat)

                self.stat_null_crit_lower = st.norm.ppf(self.alpha)
                self.stat_null_crit_upper = st.norm.ppf(1 - self.alpha)

            self.conf_int_null_crit = (self.prop_null + self.stat_null_crit_lower * \
                np.sqrt(self.prop_null * (1 - self.prop_null)
                          * (1 / trials_null)),
                self.prop_null + self.stat_null_crit_upper * np.sqrt(self.prop_null * \
                    (1 - self.prop_null)
                          * (1 / trials_null))
            )

            self.beta = 1 - self.calculate_power(self.stat)

            if self.right_tailed_flag:
                self.power_curve = {
                    temp_moving_prop: self.calculate_power(
                        self.calculate_stat(temp_moving_prop)
                    )
                    for temp_moving_prop in \
                        np.arange(self.prop_null, 1.005, 0.005)
                }

            else:
                self.power_curve = {
                    temp_moving_prop: self.calculate_power(
                        self.calculate_stat(temp_moving_prop)
                    )
                    for temp_moving_prop in \
                        np.arange(0, self.prop_null + 0.005, 0.005)
                }
        else:
            if self.is_t_test:
                if self.right_tailed_flag:
                    self.pvalue = st.t.cdf(-self.stat,
                                           df=trials_null + trials_alt - 2) * 2
                else:
                    self.pvalue = st.t.cdf(
                        self.stat, df=trials_null + trials_alt - 2) * 2

                self.stat_null_crit_lower = st.t.ppf(self.alpha / 2)
                self.stat_null_crit_upper = st.t.ppf(1 - self.alpha / 2)

            else:
                if self.right_tailed_flag:
                    self.pvalue = st.norm.cdf(-self.stat) * 2
                else:
                    self.pvalue = st.norm.cdf(self.stat) * 2

                self.stat_null_crit_lower = st.norm.ppf(self.alpha / 2)
                self.stat_null_crit_upper = st.norm.ppf(1 - self.alpha / 2)

            self.conf_int_null_crit = (self.prop_null + self.stat_null_crit_lower *
                                       np.sqrt(self.prop_null *
                                               (1 -
                                                self.prop_null) *
                                               (1 /
                                                trials_null)), self.prop_null +
                                       self.stat_null_crit_upper *
                                       np.sqrt(self.prop_null *
                                               (1 -
                                                self.prop_null) *
                                               (1 /
                                                   trials_null)), )

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

        prop_pooled = (self.success_null + moving_success_alt) / (self.trials_null + self.trials_alt)

        variance = ((prop_pooled) * (1 - prop_pooled) * ((1 / self.trials_null) + (1 / self.trials_alt)))

        stat = diff_prop / np.sqrt(variance)

        return stat

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

        if self.is_t_test:
            dist_alt = st.t(loc=stat, df=self.trials_null + self.trials_alt - 2)
        else:
            dist_alt = st.norm(loc=stat)

        if self.right_tailed_flag:
            beta = dist_alt.cdf(self.stat_null_crit_upper)
        else:
            beta = 1 - dist_alt.cdf(self.stat_null_crit_lower)

        return 1 - beta

    def get_sample_size(self, beta=0.1):
        """
        Calculate required sample size per group to obtain provided beta.

        Parameters
        ----------
        beta : float
            Type 2 error rate.

        Returns
        -------
        n : int
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
                effect_size=es,
                alpha=self.alpha,
                power=1 - beta,
                alternative='smaller')

        return int(np.round(n, 0))

    def plot_power_curve(self, figsize=(9, 6)):
        """
        Plot power curve for provided experiment parameters.

        Parameters
        ----------
        figsize : tuple, default = (9,6)
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

        sns.set_style("whitegrid")
        plt.figure(figsize=figsize)
        plt.title("Power Curve")
        sns.lineplot(
            plot_power_curve_proportion,
            plot_power_curve_values,
            color='blue')
        plt.scatter(
            self.prop_alt,
            1 -
            self.beta,
            color='#0b559f',
            label='Power at alternate proportion %s' %
            (str(
                np.round(
                    1 -
                    self.beta,
                    3))))
        plt.legend()
        plt.xlabel("Comparison Proportion")
        plt.ylabel("Power")
        plt.show()

    def print_freq_results(self):
        """
        Print Frequentist Experiment Results
        """
        is_significant = False

        if self.pvalue < self.alpha:
            is_significant = True

        print("pyAB Summary\n============\n")
        print("Test Parameters\n_______________\n")
        print("Variant A: Success Rate %s, Sample Size %s" %
              (self.prop_null, self.trials_null))
        print(
            "Variant B: Success Rate %s, Sample Size %s" %
            (self.prop_alt, self.trials_alt))
        print(
            "Type-I Error: %s, %s test\n" %
            (self.alpha, self.alt_hypothesis))
        print("Test Results\n____________\n")
        print("Test Stat: %s" % (np.round(self.stat, 3)))
        print("p-value: %s" % (np.round(self.pvalue, 3)))
        print("Type-II Error: %s" % (np.round(self.beta, 3)))
        print("Power: %s\n" % (np.round(1 - self.beta, 3)))

        if is_significant:
            print(
                "There is a statistically significant difference in proportions of two variants.\n")
        else:
            print(
                "There is no statistically significant difference in proportions of two variants.\n")

        self.plot_power_curve()


class ABTestBayesian:
    """
    Bayesian A/B Testing.

    Parameters
    ----------
    success_prior : int
        Number of successful samples from prior.

    trials_prior : int
        Number of trials from prior.
    """

    def __init__(self, success_prior, trials_prior):

        self.success_prior = success_prior
        self.trials_prior = trials_prior
        self.faliure_prior = self.trials_prior - self.success_prior

        check_valid_input(success_prior, trials_prior)

    def conduct_experiment(self, success_null, trials_null, success_alt, trials_alt,
        uplift_method='uplift_percent', num_simulations=1000):
        """
        Conduct experiment & generate uplift distributions.

        Parameters
        ----------
        success_null : int
            Number of successful samples for variant-a.

        trials_null : int
            Number of trials for variant-a.

        success_alt : int
            Number of successful samples for variant-b.

        trials_alt : int
            Number of trials for variant-b.

        num_simulations : int
            Number of mcmc simulations.

        uplift_method : str, default = 'uplift_percent'
            Uplift evaluation metric.

            * 'uplift_percent':
                percent uplift gain from variant-a to variant-b
            * 'uplift_ratio':
                uplift ratio of variant-b & variant-a
            * 'uplift_difference':
                uplift difference between variant-b & variant-a
        """

        all_uplift_methods = [
            'uplift_percent',
            'uplift_ratio',
            'uplift_difference']

        if uplift_method not in all_uplift_methods:
            raise ValueError(
                "ABTestBayesian class supports uplift methods in %s, got %s"
                % (all_uplift_methods, uplift_method)
            )

        self.num_simulations = num_simulations
        self.uplift_method = uplift_method

        check_valid_input(success_null, trials_null)
        check_valid_input(success_alt, trials_alt)

        self.success_null = success_null
        self.trials_null = trials_null

        self.success_alt = success_alt
        self.trials_alt = trials_alt

        faliure_null = self.trials_null - self.success_null
        faliure_alt = self.trials_alt - self.success_alt

        self.success_posterior_null = self.success_prior + self.success_null
        self.faliure_posterior_null = self.faliure_prior + faliure_null

        self.success_posterior_alt = self.success_prior + self.success_alt
        self.faliure_posterior_alt = self.faliure_prior + faliure_alt

        beta_x = np.arange(0, 1.005, 0.005)

        beta_prior_pdf = st.beta.pdf(
            beta_x, self.success_prior, self.faliure_prior)

        beta_null_pdf = st.beta.pdf(
            beta_x,
            self.success_posterior_null,
            self.faliure_posterior_null)

        beta_alt_pdf = st.beta.pdf(
            beta_x,
            self.success_posterior_alt,
            self.faliure_posterior_alt)

        self.uplift_dist, self.uplift_area = self.calculate_uplift_area()

        self.print_bayesian_results()

    def calculate_uplift_area(self):
        """
        Calculate Uplift pdf & area beyond threshold.

        Returns
        -------
        uplift_distribution : ndarray
            uplift distribution based on chosen uplift method.

        uplift_area : float
            percentage area above threshold.
        """

        beta_mcmc_null = st.beta.rvs(self.success_posterior_null, self.faliure_posterior_null,
            size=self.num_simulations)

        beta_mcmc_alt = st.beta.rvs(self.success_posterior_alt, self.faliure_posterior_alt,
            size=self.num_simulations)

        if self.uplift_method == 'uplift_percent':
            uplift_dist = (beta_mcmc_alt - beta_mcmc_null) / beta_mcmc_null
            uplift_area = len(uplift_dist[uplift_dist >= 0]) / len(np.abs(uplift_dist))

        elif self.uplift_method == 'uplift_ratio':
            uplift_dist = beta_mcmc_alt / beta_mcmc_null
            uplift_area = len(uplift_dist[uplift_dist >= 1]) / len(np.abs(uplift_dist))

        elif self.uplift_method == 'uplift_difference':
            uplift_dist = beta_mcmc_alt - beta_mcmc_null
            uplift_area = len(uplift_dist[uplift_dist >= 0]) / len(np.abs(uplift_dist))

        return uplift_dist, uplift_area

    def plot_uplift_distributions(self, figsize=(18, 6)):
        """
        Plot uplift pdf & cdf for provided experiment parameters.

        Parameters
        ----------
        figsize : tuple, default = (18, 6)
            matplotlib plot size.
        """

        sns.set_style("whitegrid")

        plt.figure(figsize=figsize)
        plt.subplot(1, 2, 1)
        plt.title("Uplift Distribution Plot")
        ax = sns.kdeplot(self.uplift_dist, shade=True, color='black')
        kde_x, kde_y = ax.lines[0].get_data()

        if self.uplift_method == 'uplift_ratio':
            cutoff_point = 1
            cutoff_line = plt.axvline(x=cutoff_point, linestyle='--', color='black')
        else:
            cutoff_point = 0
            cutoff_line = plt.axvline(x=cutoff_point, linestyle='--', color='black')

        ax.fill_between(kde_x, kde_y, where=(kde_x <= cutoff_point), interpolate=True,
            color='orange', alpha=0.6)
        ax.fill_between(kde_x, kde_y, where=(kde_x > cutoff_point), interpolate=True,
            color='lightgreen', alpha=0.6)

        plt.xlabel("Uplift")
        plt.ylabel("Density")
        plt.subplot(1, 2, 2)
        plt.title("Uplift Cumulative Distribution Plot")
        sns.kdeplot(self.uplift_dist, cumulative=True, color='blue', shade=True)
        plt.xlabel("Cumulative Uplift")
        plt.ylabel("Density")
        plt.show()

    def print_bayesian_results(self):
        """
        Print Bayesian Experiment Results
        """

        print("pyAB Summary\n============\n")
        print("Test Parameters\n_______________\n")
        print("Variant A: Successful Trials %s, Sample Size %s" %
              (self.success_null, self.trials_null))
        print("Variant B: Successful Trials %s, Sample Size %s" %
              (self.success_alt, self.trials_alt))
        print("Prior: Successful Trials %s, Sample Size %s\n" %
              (self.success_prior, self.trials_prior))
        print("Test Results\n____________\n")
        print("Evaluation Metric: %s" % (self.uplift_method))
        print("Number of mcmc simulations: %s\n" % (self.num_simulations))

        if self.uplift_method == 'uplift_percent':
            print("%s %% simulations show Uplift Gain Percent above 0.\n" %
                  (np.round(self.uplift_area * 100, 2)))
        elif self.uplift_method == 'uplift_ratio':
            print("%s %% simulations show Uplift Ratio above 1.\n" %
                  (np.round(self.uplift_area * 100, 2)))
        elif self.uplift_method == 'uplift_difference':
            print("%s %% simulations show Uplift Difference above 0.\n" %
                  (np.round(self.uplift_area * 100, 2)))

        self.plot_uplift_distributions()

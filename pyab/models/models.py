"""Main file comprising Uplift models."""

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.utils.validation import check_consistent_length
from sklearn.utils.multiclass import type_of_target

class UpliftClassTransformation(BaseEstimator):
    """
    UpliftClassTransformation A/B Testing aka Two sample proportion test.

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

    def __init__(self, estimator):
        self.estimator = estimator

    def fit(self, X, y, treatment, estimator_params=None):

        check_consistent_length(X, y, treatment)

        if type_of_target(y) != 'binary' or type_of_target(treatment) != 'binary':
            raise ValueError(
                "UpliftClassTransformation expects binary class & treatment labels."
            )

        z = y*treatment + (1-y)*(1-treatment)

        if estimator_params is None:
            estimator_params = {}

        self.estimator.fit(X, z, **estimator_params)

        return self

    def predict(self, X, num_deciles=10):

        uplift = 2*(self.estimator.predict_proba(X)[:, 1]) - 1

        df_uplift = pd.DataFrame({'uplift': uplift})
        df_uplift.sort_values('uplift', ascending=False, inplace=True)
        df_uplift['decile'] = pd.qcut(df_uplift['uplift'], num_deciles, labels=False)

        return uplift

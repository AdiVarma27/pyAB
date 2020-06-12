********
**pyAB**
********
pyAB is a Python package for Bayesian & Frequentist A/B Testing.



Features:
#########


**Bayesian A/B Test**:

- Conduct quick experiments to check for winning variant with additional prior information (Beta Distribution parameters).
- Try different evaluation metrics (Uplift Ratio, Uplift Difference & Uplift Percent Gain) & vary MCMC simulation sample size per variant.
- Visualize & inspect Uplift Density & Cumulative Density distributions.

**Frequentist A/B Test**:

- Conduct quick experiments to check for winning variant using two sample proportion test (Statistical significance).
- Estimate required sample size per variant to reach provided Type-II error rate.
- Visualize & inspect power curve for varying alternative proportions.

.. toctree::
   :hidden:

   self

.. toctree::
   :maxdepth: 2
   :caption: Content

   install
   quick_start
   api
   contributing
   release_history


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
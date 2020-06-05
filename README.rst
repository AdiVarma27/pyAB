.. image:: https://readthedocs.org/projects/pyab/badge/?version=latest
  :target: https://pyab.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status
 
====
pyAB
====
pyAB is a Python package for Frequentist & Bayesian A/B Testing.


Features:
--------
- Conduct quick experiments to check for winning variant (statistical significance).
- Visualize & inspect power curve for varying alternative proportions.
- Estimate required sample size per variant to reach expected Type-II error rate.

Installation:
------------
Best way to install pyAB is through pip

.. code:: python

   pip install pyAB

To install from source, use the following Github link

.. code:: python

   git clone https://github.com/AdiVarma27/pyAB.git
   cd pyAB
   python setup.py install

Dependencies:
------------

pyAB has the following dependencies:

- numpy
- matplotlib
- seaborn
- scipy
- statsmodels

Documentation:
-------------

pyAB documentation is available at `pyab.readthedocs.io <https://pyab.readthedocs.io/en/latest/>`_ & `pyab.rtfd.io <https://pyab.rtfd.io/en/latest/>`_.


Quick Start:
------------

.. code:: python

   from pyab.experiments import ABTestFrequentist

   ad_experiment = ABTestFrequentist(alpha=0.05, alt_hypothesis='one_tailed')

   stat, pvalue = ad_experiment.conduct_experiment(success_null=100, trials_null=1000, 
                                 success_alt=125, trials_alt=1000)

License:
-------

`MIT License Copyright (c) 2020 <https://github.com/AdiVarma27/pyAB/blob/master/LICENSE>`_

import os
from setuptools import setup

setup(name='pyAB',
      version='10.3.4',
      description='A/B Testing using Bayesian & Frequentist Statistics',
      url='https://github.com/AdiVarma27/pyAB',
      author='Aditya Varma Kalidindi',
      author_email='kadityavarma27@gmail.com',
      install_requires = ['matplotlib', 'numpy>=1.13', 'scipy==1.2.0', 'seaborn==0.9.0', 'statsmodels==0.9.0']
    )

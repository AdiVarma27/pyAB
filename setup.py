import os
from setuptools import setup, find_packages

setup(name='pyAB',
      version='20.0.1',
      description='A/B Testing using Bayesian & Frequentist Statistics',
      url='https://github.com/AdiVarma27/pyAB',
      author='Aditya Varma Kalidindi',
      author_email='kadityavarma27@gmail.com',
      packages=find_packages(),
      install_requires = ['matplotlib','numpy>=1.13','scipy==1.2.0','seaborn==0.9.0','statsmodels']
    )

import os
from setuptools import setup, find_packages


cwd = os.getcwd()
with open(cwd + '/requirements.txt', encoding="utf-8") as req_file:
    REQUIRED_PACKAGES = [line.rstrip() for line in req_file]


setup(name='pyAB',
      version='10.0.1',
      description='A/B Testing using Bayesian & Frequentist Statistics',
      url='https://github.com/AdiVarma27/pyAB',
      author='Aditya Varma Kalidindi',
      author_email='kadityavarma27@gmail.com',
      install_requires = REQUIRED_PACKAGES,
      packages=find_packages(),
)
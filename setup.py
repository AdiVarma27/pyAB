import os
from setuptools import setup

curr_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(curr_path, 'requirements.txt'), encoding="utf-8") as req_file:
    REQUIRED_PACKAGES = [line.rstrip() for line in req_file]


setup(name='pyAB',
      version='5.1.0',
      description='A/B Testing using Bayesian & Frequentist Statistics',
      url='https://github.com/AdiVarma27/pyAB',
      author='Aditya Varma Kalidindi',
      author_email='kadityavarma27@gmail.com',
      install_requires = REQUIRED_PACKAGES,
)
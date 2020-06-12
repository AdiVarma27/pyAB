import os
from setuptools import setup, find_packages

curr_path = os.path.abspath(os.path.dirname(__file__))

files = os.listdir(os.curdir)

with open('requirements.txt', encoding="utf-8") as req_file:
    REQUIRED_PACKAGES = [line.rstrip() for line in req_file]


setup(name='pyAB',
      version='5.1.4',
      description='A/B Testing using Bayesian & Frequentist Statistics',
      url='https://github.com/AdiVarma27/pyAB',
      author='Aditya Varma Kalidindi',
      author_email='kadityavarma27@gmail.com',
      install_requires = REQUIRED_PACKAGES,
      packages=find_packages(),
)
from setuptools import setup

with open('requirements.txt') as req_file:
    REQUIRED_PACKAGES = [line.rstrip() for line in req_file]


setup(name='pyAB',
      version='0.0.1',
      description='A/B Testing using Bayesian & Frequentist Statistics',
      url='https://github.com/AdiVarma27/pyAB',
      author='Aditya Varma Kalidindi',
      author_email='kadityavarma27@gmail.com',
      install_requires = REQUIRED_PACKAGES,
)
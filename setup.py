from setuptools import setup
from sys import version_info

with open('README.rst') as README:
    long_description = README.read()
    long_description = long_description[long_description.index('Description'):]

if (version_info < (2, 7)) or ((3, 0) <= version_info < (3, 4)):
    pytest_runner = 'pytest-runner<=3.0'
else:
    pytest_runner = 'pytest-runner'

setup(name='poloniex',
      version='0.0.14',
      description='Poloniex API client for humans',
      long_description=long_description,
      url='http://github.com/Aula13/poloniex',
      author='Enrico Bacis, Daniele Ciriello',
      author_email='enrico.bacis@gmail.com, ciriello.daniele@gmail.com',
      license='MIT',
      packages=['poloniex'],
      setup_requires=[pytest_runner],
      install_requires=['requests', 'six'],
      tests_require=['pytest', 'responses'],
      keywords='poloniex cryptocurrency cryptocurrencies api client bitcoin'
      )

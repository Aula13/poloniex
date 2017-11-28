from setuptools import setup

with open('README.rst') as README:
    long_description = README.read()
    long_description = long_description[long_description.index('Description'):]

setup(name='poloniex',
      version='0.0.11',
      description='Poloniex API client for humans',
      long_description=long_description,
      url='http://github.com/Aula13/poloniex',
      author='Enrico Bacis, Daniele Ciriello',
      author_email='enrico.bacis@gmail.com, ciriello.daniele@gmail.com',
      license='MIT',
      packages=['poloniex'],
      setup_requires=['pytest-runner'],
      install_requires=['requests', 'six'],
      tests_require=['pytest', 'responses'],
      keywords='poloniex cryptocurrency cryptocurrencies api client bitcoin'
      )

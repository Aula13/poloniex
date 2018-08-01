poloniex
########

*Poloniex python API client for humans*

.. image:: https://travis-ci.org/Aula13/poloniex.svg?branch=master
    :target: https://travis-ci.org/Aula13/poloniex
    
.. image:: https://badge.fury.io/py/poloniex.svg
    :target: https://badge.fury.io/py/poloniex
    :alt: Code coverage

Description
-----------

`Poloniex API`_ client for humans

Installation
------------

The package has been uploaded to `PyPI`_, so you can install it with pip:

.. code:: bash

   $ pip install poloniex

Usage Examples
--------------

Documentation can be inspected by calling the python's ``help`` function with a
``Poloniex`` object as parameter:

.. code:: python

   from poloniex import Poloniex
   polo = Poloniex()
   help(polo)


Public APIs
"""""""""""

.. code:: python

   from poloniex import Poloniex
   polo = Poloniex()
   ticker = polo.returnTicker()['BTC_ETH']
   print(ticker)


Private APIs
""""""""""""

.. code:: python

   from poloniex import Poloniex
   import os

   api_key = os.environ.get('POLONIEX_API_KEY')
   api_secret = os.environ.get('POLONIEX_SECRET')
   polo = Poloniex(api_key, api_secret)

   ticker = polo.returnTicker()['BTC_ETH']
   print(ticker)

   balances = polo.returnBalances()
   print(balances)


Used in
-------

* `crypto_trader`_: Trading automation on poloniex cyriptocoin exchange


Common Errors
-------------

If you are having a nonce error or an exception like this one below, you probably need to generate a new api key-secret pair.

.. code:: python

        Traceback (most recent call last):
          File "C:/Users/name/.PyCharmCE2018.2/config/scratches/scratch.py", line 10, in <module>
            balances = polo.returnBalances()
          File "C:\Users\name\AppData\Roaming\Python\Python27\site-packages\poloniex\poloniex.py", line 183, in returnBalances
            return self._private('returnBalances')
          File "C:\Users\name\AppData\Roaming\Python\Python27\site-packages\poloniex\poloniex.py", line 50, in _fn
            raise PoloniexCommandException(respdata['error'])
        poloniex.exceptions.PoloniexCommandException: Nonce must be greater than 1532206573738226. You provided 1533067257748.

        Process finished with exit code 1


Donations
---------

BTC     13NpLwXgEP8d9NpDUHptY6BypFRNXHL3tr

.. _PyPI: https://pypi.python.org/pypi/poloniex
.. _Poloniex API: https://poloniex.com/support/api/
.. _crypto_trader: https://github.com/timucin/cyripto_trader

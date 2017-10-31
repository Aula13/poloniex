poloniex
########

*Poloniex python API client for humans*

.. image:: https://travis-ci.org/Aula13/poloniex.svg?branch=master
    :target: https://travis-ci.org/Aula13/poloniex

Description
-----------

Alpha version of a `Poloniex API`_ client for humans

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


Donations
---------

=================  ======  ==========================================
Name               Symbol  Address
=================  ======  ==========================================
Bitcoin            BTC     13NpLwXgEP8d9NpDUHptY6BypFRNXHL3tr
Ethereum           ETH     0x8f61777b0f951ed5df684da495d82171aa3645ea
Litecoin           LTC     LKM1eTU8BmvCECJr54Tz1pHDr4e2AS41Ai
=================  ======  ==========================================


.. _PyPI: https://pypi.python.org/pypi/poloniex
.. _Poloniex API: https://poloniex.com/support/api/
.. _crypto_trader: https://github.com/timucin/cyripto_trader

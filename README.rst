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

The package has been uploaded to `PyPI`_, so you can install it with pip::

    $pip install poloniex
    
    
Usage Examples
-----

Documentation can be inspected by calling the python's ``help`` function with a ``Poloniex`` object as parameter::

    >>> from poloniex import Poloniex
    >>> polo = Poloniex()
    >>> help(polo)
     
     
     
**Public APIs:** ::

    from poloniex import Poloniex
     
    polo = Poloniex()
     
    ticker = p.returnTicker()['BTC_ETH']
    print(ticker)
     
     
**Private APIs:**::

    import os
    from poloniex import Poloniex
     
    api_key = os.environ.get('POLONIEX_API_KEY')
    api_secret = os.environ.get('POLONIEX_SECRET')
     
    polo = Poloniex(api_key, api_secret)
          
    ticker = p.returnTicker()['BTC_ETH']
    print(ticker)
     
    balances = polo.returnBalances()
    print(balances)



Donations
---------

=================  ======  ====== 
Name               Symbol  Address 
=================  ======  ====== 
Bitcoin            BTC     13NpLwXgEP8d9NpDUHptY6BypFRNXHL3tr 
Ethereum           ETH     0x8f61777b0f951ed5df684da495d82171aa3645ea 
Litecoin           LTC     LKM1eTU8BmvCECJr54Tz1pHDr4e2AS41Ai
Ethereum Classic   ETC     0xb564911a90b6f37ce9bd756f44e91cdf8475b402
=================  ======  ======


.. _PyPI: https://pypi.python.org/pypi/poloniex
.. _Poloniex API: https://poloniex.com/support/api/

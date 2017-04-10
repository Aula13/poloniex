import hmac as _hmac
import time as _time
import hashlib as _hashlib
import requests as _requests
import functools as _functools
import itertools as _itertools
import threading as _threading

from .utils import AutoCastDict
from .exceptions import *


_PUBLIC_URL = 'https://poloniex.com/public'
_PRIVATE_URL = 'https://poloniex.com/tradingApi'


class PoloniexPublic(object):

    """Client to connect to Poloniex public APIs"""

    def __init__(self, public_url=_PUBLIC_URL, limit=6):
        """Initialize Poloniex client."""
        self._public_url = public_url
        self._public_session = _requests.Session()
        self._semaphore = _threading.Semaphore(limit)

    @staticmethod
    def _sanitize_parameters(params):
        """Sanitize the params removing none values."""
        return {key: val for key, val in params.items() if val is not None}

    def _public(self, command, **params):
        """Invoke the 'command' public API with optional params."""
        params = self._sanitize_parameters(params)
        params['command'] = command
        response = self._public_session.get(self._public_url, params=params)
        return response.json(object_hook=AutoCastDict)

    def returnTicker(self):
        """Returns the ticker for all markets."""
        return self._public('returnTicker')

    def return24hVolume(self):
        """Returns the 24-hour volume for all markets, plus totals for
        primary currencies."""
        return self._public('return24hVolume')

    def returnOrderBook(self, currencyPair='all', depth='50'):
        """Returns the order book for a given market, as well as a sequence
        number for use with the Push API and an indicator specifying whether
        the market is frozen. You may set currencyPair to "all" to get the
        order books of all markets."""
        return self._public('returnOrderBook', currencyPair=currencyPair,
                            depth=depth)

    def returnTradeHistory(self, currencyPair, start=None, end=None):
        """Returns the past 200 trades for a given market, or up to 50,000
        trades between a range specified in UNIX timestamps by the "start"
        and "end" GET parameters."""
        return self._public('returnTradeHistory', currencyPair=currencyPair,
                            start=start, end=end)

    def returnChartData(self, currencyPair, period, start, end):
        """Returns candlestick chart data. Required GET parameters are
        "currencyPair", "period" (candlestick period in seconds; valid values
        are 300, 900, 1800, 7200, 14400, and 86400), "start", and "end".
        "Start" and "end" are given in UNIX timestamp format and used to
        specify the date range for the data returned."""
        return self._public('returnChartData', currencyPair=currencyPair,
                            period=period, start=start, end=end)

    def returnCurrencies(self):
        """Returns information about currencies."""
        return self._public('returnCurrencies')

    def returnLoanOrders(self, currency):
        """Returns the list of loan offers and demands for a given currency,
        specified by the "currency" GET parameter."""
        return self._public('returnLoanOrders', currency=currency)


class Poloniex(PoloniexPublic):

    """Client to connect to Poloniex private APIs."""

    class _PoloniexAuth(_requests.auth.AuthBase):

        """Poloniex Request Authentication."""

        def __init__(self, secret):
            self._secret = secret

        def __call__(self, request):
            signature = _hmac.new(self._secret, request.body, _hashlib.sha512)
            request.headers['Sign'] = signature.hexdigest()
            return request

    def __init__(self, apikey=None, secret=None, public_url=_PUBLIC_URL,
                 private_url=_PRIVATE_URL, limit=6):
        """Initialize the Poloniex private client."""
        PoloniexPublic.__init__(self, public_url, limit)
        self._private_url = private_url
        self._private_session = _requests.Session()
        self._private_session.headers['Key'] = self._apikey = apikey
        self._secret = secret
        self._nonces = _itertools.count(int(_time.time() * 1000))

    def _private(self, command, **params):
        """Invoke the 'command' public API with optional params."""
        if not self._apikey or not self._secret:
            raise PoloniexCredentialsException('missing apikey/secret')

        params = self._sanitize_parameters(params)
        params.update({'command': command, 'nonce': next(self._nonces)})
        response = self._private_session.post(self._private_url,
                                              data=params, auth=Poloniex._PoloniexAuth(self._secret))
        return response.json(object_hook=AutoCastDict)

    def returnBalances(self):
        """Returns all of your available balances."""
        return self._private('returnBalances')

    def returnCompleteBalances(self, account=None):
        """Returns all of your balances, including available balance, balance
        on orders, and the estimated BTC value of your balance. By default,
        this call is limited to your exchange account; set the "account" POST
        parameter to "all" to include your margin and lending accounts."""
        return self._private('returnCompleteBalances', account=account)

    def returnDepositAddresses(self):
        """Returns all of your deposit addresses."""
        return self._private('returnDepositAddresses')

    def generateNewAddress(self, currency):
        """Generates a new deposit address for the currency specified by the
        "currency" POST parameter. Only one address per currency per day may be
        generated, and a new address may not be generated before the
        previously-generated one has been used."""
        return self._private('generateNewAddress', currency=currency)

    def returnDepositsWithdrawals(self, start, end):
        """Returns your deposit and withdrawal history within a range,
        specified by the "start" and "end" POST parameters, both of which
        should be given as UNIX timestamps."""
        return self._private('returnDepositsWithdrawals', start=start, end=end)

    def returnOpenOrders(self, currencyPair='all'):
        """Returns your open orders for a given market, specified by the
        "currencyPair" POST parameter, e.g. "BTC_XCP". Set "currencyPair" to
        "all" to return open orders for all markets."""
        return self._private('returnOpenOrders', currencyPair=currencyPair)

    def returnTradeHistory(self, currencyPair='all', start=None, end=None):
        """Returns your trade history for a given market, specified by the
        "currencyPair" POST parameter. You may specify "all" as the
        currencyPair to receive your trade history for all markets. You may
        optionally specify a range via "start" and/or "end" POST parameters,
        given in UNIX timestamp format; if you do not specify a range, it will
        be limited to one day."""
        return self._private('returnTradeHistory', currencyPair=currencyPair,
                             start=start, end=end)

    def returnTradeHistoryPublic(self, currencyPair, start=None, end=None):
        """Returns the past 200 trades for a given market, or up to 50,000
        trades between a range specified in UNIX timestamps by the "start"
        and "end" GET parameters."""
        PoloniexPublic.returnTradeHistory(self, currencyPair, start, end)

    def returnOrderTrades(self):
        """Returns all trades involving a given order, specified by the
        "orderNumber" POST parameter. If no trades for the order have occurred
        or you specify an order that does not belong to you, you will receive
        an error. """
        raise NotImplementedError

    def buy(self):
        """Places a limit buy order in a given market. Required POST parameters
         are "currencyPair", "rate", and "amount". If successful, the method
         will return the order number.
        You may optionally set "fillOrKill", "immediateOrCancel", "postOnly"
        to 1. A fill-or-kill order will either fill in its entirety or be
        completely aborted. An immediate-or-cancel order can be partially or
        completely filled, but any portion of the order that cannot be filled
        immediately will be canceled rather than left on the order book.
        A post-only order will only be placed if no portion of it fills
        immediately; this guarantees you will never pay the taker fee on any
        part of the order that fills."""
        raise NotImplementedError

    def sell(self):
        """Places a sell order in a given market. Parameters and output are
        the same as for the buy method."""
        raise NotImplementedError

    def cancelOrder(self):
        """Cancels an order you have placed in a given market. Required POST
        parameter is "orderNumber"."""
        return

    def moveOrder(self):
        """Cancels an order and places a new one of the same type in a single
        atomic transaction, meaning either both operations will succeed or both
         will fail. Required POST parameters are "orderNumber" and "rate"; you
         may optionally specify "amount" if you wish to change the amount of
         the new order. "postOnly" or "immediateOrCancel" may be specified for
         exchange orders, but will have no effect on margin orders. """
        raise NotImplementedError

    def withdraw(self):
        """Immediately places a withdrawal for a given currency, with no email
        confirmation. In order to use this method, the withdrawal privilege
        must be enabled for your API key. Required POST parameters are
        "currency", "amount", and "address". For XMR withdrawals, you may
        optionally specify "paymentId"."""
        raise NotImplementedError

    def returnFeeInfo(self):
        """If you are enrolled in the maker-taker fee schedule, returns your
        current trading fees and trailing 30-day volume in BTC. This
        information is updated once every 24 hours."""
        raise NotImplementedError

    def returnAvailableAccountBalances(self):
        """Returns your balances sorted by account. You may optionally specify
        the "account" POST parameter if you wish to fetch only the balances of
        one account. Please note that balances in your margin account may not
        be accessible if you have any open margin positions or orders."""
        raise NotImplementedError

    def returnTradableBalances(self):
        """Returns your current tradable balances for each currency in each
        market for which margin trading is enabled. Please note that these
        balances may vary continually with market conditions."""
        raise NotImplementedError

    def transferBalance(self):
        """Transfers funds from one account to another (e.g. from your exchange
         account to your margin account). Required POST parameters are
         "currency", "amount", "fromAccount", and "toAccount"."""
        raise NotImplementedError

    def returnMarginAccountSummary(self):
        """Returns a summary of your entire margin account. This is the same
        information you will find in the Margin Account section of the Margin
        Trading page, under the Markets list. """
        raise NotImplementedError

    def marginBuy(self):
        """Places a margin buy order in a given market. Required POST
        parameters are "currencyPair", "rate", and "amount". You may optionally
         specify a maximum lending rate using the "lendingRate" parameter.
         If successful, the method will return the order number and any trades
         immediately resulting from your order."""
        raise NotImplementedError

    def marginSell(self):
        """Places a margin sell order in a given market. Parameters and output
        are the same as for the marginBuy method."""
        raise NotImplementedError

    def getMarginPosition(self):
        """Returns information about your margin position in a given market,
        specified by the "currencyPair" POST parameter. You may set
        "currencyPair" to "all" if you wish to fetch all of your margin
        positions at once. If you have no margin position in the specified
        market, "type" will be set to "none". "liquidationPrice" is an
        estimate, and does not necessarily represent the price at which an
        actual forced liquidation will occur. If you have no liquidation
        price, the value will be -1. """
        raise NotImplementedError

    def closeMarginPosition(self, currencyPair):
        """Closes your margin position in a given market (specified by the
        "currencyPair" POST parameter) using a market order. This call will
        also return success if you do not have an open position in the
        specified market."""
        return self._private('closeMarginPosition', currencyPair=currencyPair)

    def createLoanOffer(self, currency, amount, duration, autoRenew,
                        lendingRate):
        """Creates a loan offer for a given currency. Required POST parameters
        are "currency", "amount", "duration", "autoRenew" (0 or 1), and
        "lendingRate". """
        return self._private('createLoanOffer', currency=currency,
                             amount=amount, duration=duration,
                             autoRenew=autoRenew, lendingRate=lendingRate)

    def cancelLoanOffer(self, orderNumber):
        """Cancels a loan offer specified by the "orderNumber" POST
        parameter."""
        return self._private('cancelLoanOffer', orderNumber=orderNumber)

    def returnOpenLoanOffers(self):
        """Returns your open loan offers for each currency. """
        return self._private('returnOpenLoanOffers')

    def returnActiveLoans(self):
        """Returns your active loans for each currency."""
        return self._private('returnActiveLoans')

    def returnLendingHistory(self, start, stop, limit=None):
        """Returns your lending history within a time range specified by the
        "start" and "end" POST parameters as UNIX timestamps. "limit" may also
        be specified to limit the number of rows returned. """
        return self._private('returnLendingHistory', start=start, stop=stop,
                             limit=limit)

    def toggleAutoRenew(self, orderNumber):
        """Toggles the autoRenew setting on an active loan, specified by the
        "orderNumber" POST parameter. If successful, "message" will indicate
        the new autoRenew setting. """
        return self._private('toggleAutoRenew', orderNumber=orderNumber)

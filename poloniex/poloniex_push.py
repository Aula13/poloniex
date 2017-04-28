from __future__ import print_function

import six as _six

from autobahn.asyncio.wamp import ApplicationSession as _ApplicationSession
from autobahn.asyncio.wamp import ApplicationRunner as _ApplicationRunner
from trollius import coroutine as _coroutine, From as _From


class Session(_ApplicationSession):

    def onConnect(self):
        self.join(self.config.realm)

    @_coroutine
    def onJoin(self, details):
        def onTicker(*args, **kwargs):
            self.config.extra['backFunction'](args, kwargs)

        feed = self.config.extra['feed']

        yield _From(self.subscribe(onTicker, feed))


class PoloniexPush():
    '''
    Alternatively, you can instantiate the PoloniexPush class and call the feed function to use this as a module
    i.e.
    >> from wss_client import PoloniexPush
    >> ticker_feed = PoloniexPush('ticker')
    >> print(ticker_feed.feed())
    '''

    def __init__(self, feed, backFunction):
        self.feed = _six.u(feed)
        self.backFunction = backFunction

    def feed(self):
        runner = _ApplicationRunner(u"wss://api.poloniex.com:443", u"realm1", extra={'feed': self.feed, 'backFunction': self.backFunction})
        return runner.run(Session)


def main():
    def onOrderBookTrades(*args, **kwargs):
        print("Order Book or Trade update received:", args, kwargs)

    def onTicker(*args, **kwargs):
        print("Event received:", args)

    runner = _ApplicationRunner(u"wss://api.poloniex.com:443", u"realm1",
                                extra={'feed': u'ticker', 'backFunction': onTicker})

    runner.run(Session)

if __name__ == "__main__":
    main()

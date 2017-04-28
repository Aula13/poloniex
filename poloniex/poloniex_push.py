from __future__ import print_function

import sys as _sys
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

        topic = _six.u(self.config.extra['topic'])

        yield _From(self.subscribe(onTicker, topic))


class PoloniexPush():
    '''
    Alternatively, you can instantiate the PoloniexPush class and call the feed function to use this as a module
    i.e.
    >> from wss_client import PoloniexPush
    >> ticker_feed = PoloniexPush('ticker')
    >> print(ticker_feed.feed())
    '''

    def __init__(self, topic, backFunction):
        self.topic = topic
        self.backFunction = backFunction

    def feed(self):
        runner = _ApplicationRunner(u"wss://api.poloniex.com:443", u"realm1", extra={'topic': self.topic, 'backFunction': self.backFunction})
        return runner.run(Session)


def main():
    def onOrderBookTrades(*args, **kwargs):
        print("Order Book or Trade update received:", args, kwargs)

    def onTicker(*args, **kwargs):
        print("Event received:", args)

    runner = _ApplicationRunner(u"wss://api.poloniex.com:443", u"realm1",
                                extra={'topic': 'ticker', 'backFunction': onTicker})

    runner.run(Session)

if __name__ == "__main__":
    main()

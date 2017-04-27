from __future__ import print_function

import sys as _sys

from autobahn.asyncio.wamp import ApplicationSession as _ApplicationSession
from autobahn.asyncio.wamp import ApplicationRunner as _ApplicationRunner
from trollius import coroutine as _coroutine, From as _From


class PoloniexPush(_ApplicationSession):

    def onConnect(self):
        self.join(self.config.realm)

    @_coroutine
    def onJoin(self, details):
        def onTicker(*args, **kwargs):
            if 'onEvent' in self.config.extra:
                if kwargs:
                    self.config.extra['onEvent'](args, kwargs)
                else:
                    self.config.extra['onEvent'](args)
            else:
                print("Event received:", args, kwargs)
        if _sys.version_info >= (3, 0):
            topic = self.config.extra['topic']
        else:
            topic = unicode(self.config.extra['topic'])

        try:
            yield _From(self.subscribe(onTicker, topic))
        except Exception as e:
            print("Could not subscribe to topic: ", e)


class PushMain():
    '''
    Alternatively, you can instantiate the PushMain class and call the feed function to use this as a module
    i.e.
    >> from wss_client import PushMain
    >> ticker_feed = PushMain()
    >> print(ticker_feed.feed())
    or
    >> from wss_client import PushMain
    >> OrderBook_feed = PushMain('BTC_ETH')
    >> print(OrderBook_feed.feed())

    You will need to implement it as thread / async function if you want your program to do anything other than
    spit out the websocket feed forever and ever - unfortunately beyond my limited expertise
    '''

    def __init__(self, topic='ticker'):
        self.topic = topic

    def feed(self):
        runner = _ApplicationRunner(u"wss://api.poloniex.com:443", u"realm1", extra={'topic': self.topic})
        return runner.run(PoloniexPush)


def main():
    def onOrderBookTrades(*args, **kwargs):
        print("Order Book or Trade update received:", args, kwargs)

    runner = _ApplicationRunner(u"wss://api.poloniex.com:443", u"realm1",
                                extra={'topic': 'BTC_ETH', 'onEvent': onOrderBookTrades})

    runner.run(PoloniexPush)

if __name__ == "__main__":
    main()

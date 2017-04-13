from poloniex import PoloniexPublic
import responses
import requests

@responses.activate
def test_returnTicker():
    responses.add(responses.GET, 'https://poloniex.com/public',
            body=('{"BTC_LTC":{"last":"0.0251", "lowestAsk":"0.02589999", "highestBid":"0.0251",'
                  '  "percentChange":"0.02390438", "baseVolume":"6.16485315", "quoteVolume":"245.82513926"},'
                  ' "BTC_NXT":{"last":"0.00005730", "lowestAsk":"0.00005710", "highestBid":"0.00004903",'
                  '  "percentChange":"0.16701570", "baseVolume":"0.45347489", "quoteVolume":"9094"}}'))

    polo = PoloniexPublic()
    response = polo.returnTicker()

    assert len(responses.calls) == 1
    assert 'BTC_LTC' in response and 'BTC_NXT' in response
    assert response['BTC_LTC']['last'] == 0.0251 and response['BTC_NXT']['last'] == 0.00005730

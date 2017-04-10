class PoloniexException(Exception):
    """Generic Poloniex Exception."""
    pass

class PoloniexCredentialsException(PoloniexException, RuntimeError):
    """Missing or wrong credentials while using Private API."""
    pass

class PoloniexInvalidParametersException(PoloniexException, RuntimeError):
    """Wrong parameters while using Private API."""
    pass

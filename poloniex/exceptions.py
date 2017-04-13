class PoloniexException(Exception):
    """Generic Poloniex Exception."""
    pass


class PoloniexCredentialsException(PoloniexException, RuntimeError):
    """Missing or wrong credentials while using Trading API."""
    pass


class PoloniexCommandException(PoloniexException, RuntimeError):
    """Error in command execution."""
    pass

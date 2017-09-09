import threading
import six


# Timer's implementation class is hidden on Python2
Timer = getattr(threading, "{0}Timer".format("_" if six.PY2 else ""))


class RecurrentTimer(Timer):
    """A repetitive Timer implementation.
    See: https://hg.python.org/cpython/file/2.7/Lib/threading.py#l1079
    """

    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)

        # this should never be reached with a _thread implementation
        # but we leave it here just in case we're a custom
        # Python implementation that is messing around with _thread
        # and isn't up to standard, so we don't have an infinite
        # loop with a signal handler.
        self.finished.set()


class Semaphore(object):
    """This class implements semaphore objects.
    Semaphores manage a counter representing the number of release() calls minus
    the number of acquire() calls, plus an initial value. The acquire() method
    blocks if necessary until it can return without making the counter
    negative. If not given, value defaults to 1.

    This is a replica of the Python3 implementation with a convenience clear method.
    The reason this was duplicated rather than subclasses is because on Python2,
    the necessary value attributes are hard-private instead of soft-private.
    """
    # After Tim Peters' semaphore class, but not quite the same (no maximum)
    def __init__(self, value=1):
        if value < 0:
            raise ValueError("semaphore initial value must be >= 0")
        self._cond = threading.Condition(threading.Lock())
        self._initial = self._value = value

    def acquire(self, blocking=True, timeout=None):
        """Acquire a semaphore, decrementing the internal counter by one.
        When invoked without arguments: if the internal counter is larger than
        zero on entry, decrement it by one and return immediately. If it is zero
        on entry, block, waiting until some other thread has called release() to
        make it larger than zero. This is done with proper interlocking so that
        if multiple acquire() calls are blocked, release() will wake exactly one
        of them up. The implementation may pick one at random, so the order in
        which blocked threads are awakened should not be relied on. There is no
        return value in this case.
        When invoked with blocking set to true, do the same thing as when called
        without arguments, and return true.
        When invoked with blocking set to false, do not block. If a call without
        an argument would block, return false immediately; otherwise, do the
        same thing as when called without arguments, and return true.
        When invoked with a timeout other than None, it will block for at
        most timeout seconds.  If acquire does not complete successfully in
        that interval, return false.  Return true otherwise.
        """
        if not blocking and timeout is not None:
            raise ValueError("can't specify timeout for non-blocking acquire")
        rc = False
        endtime = None
        with self._cond:
            while self._value == 0:
                if not blocking:
                    break
                if timeout is not None:
                    if endtime is None:
                        endtime = threading._time() + timeout
                    else:
                        timeout = endtime - threading._time()
                        if timeout <= 0:
                            break
                self._cond.wait(timeout)
            else:
                self._value -= 1
                rc = True
        return rc

    __enter__ = acquire

    def release(self):
        """Release a semaphore, incrementing the internal counter by one.
        When the counter is zero on entry and another thread is waiting for it
        to become larger than zero again, wake up that thread.
        """
        with self._cond:
            self._value += 1
            self._cond.notify()

    def clear(self):
        """Release the semaphore of all of its bounds, setting the internal
        counter back to its original bind limit. Notify an equivalent amount
        of threads that they can run."""
        with self._cond:
            to_notify = self._initial - self._value
            self._value = self._initial
            self._cond.notify(to_notify)

    def __exit__(self, t, v, tb):
        self.release()

import zmqpy
from ctypes import get_errno

class ZMQError(Exception):
    def __init__(self, _errno=0):
        if not _errno:
            self._errno = get_errno()
        else:
            self._errno = _errno

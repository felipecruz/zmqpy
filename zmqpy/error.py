import zmqpy
from ctypes import get_errno

__all__ = ['ZMQError']

class ZMQError(Exception):
    def __init__(self, errno=0):
        if not errno:
            self.errno = get_errno()
        else:
            self.errno = errno

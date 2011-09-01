import sys

from zmqpy import czmq
from error import ZMQError
from constants import POLLIN, POLLOUT, POLLERR

class Poller(object):
    """Poller()

A stateful poll interface that mirrors Python's built-in poll.
"""

    def __init__(self):
        self.sockets = {}
        self._return_events = []
        self.loop = czmq.zloop_new()
        czmq.zloop_start(self.loop)

    def register(self, socket, flags=POLLIN|POLLOUT):
        if flags:
            self.sockets[socket] = flags
            callback = CMPFUNC(self._loop_callback)
            item = zmq_pollitem_t()
            
            if hasattr(socket, 'fileno'):
                item.f = socket.fileno()
            else:
                item.f = 0
            
            item.socket = socket
            item.events = flags
            
            rc = czmq.zloop_poller(self.loop, item, callback, pointer(None))
        elif socket in self.sockets:
            # uregister sockets registered with no events
            self.unregister(socket)
        else:
            # ignore new sockets with no events
            pass

    def modify(self, socket, flags=POLLIN|POLLOUT):
        self.register(socket, flags)

    def unregister(self, socket):
        del self.sockets[socket]
        
    def _loop_callback(self, loop, item, args):
        self._return_events.append((item.f, item.revents))

    def poll(self, timeout=None):
        return self._return_events


def select(rlist, wlist, xlist, timeout=None):
    """select(rlist, wlist, xlist, timeout=None) -> (rlist, wlist, xlist)

Return the result of poll as a lists of sockets ready for r/w/exception.

This has the same interface as Python's built-in ``select.select()`` function.

Parameters
----------
timeout : float, int, optional
The timeout in seconds. If None, no timeout (infinite). This is in seconds to be
compatible with ``select.select()``. The underlying zmq_poll uses microseconds
and we convert to that in this function.
rlist : list of sockets/FDs
sockets/FDs to be polled for read events
wlist : list of sockets/FDs
sockets/FDs to be polled for write events
xlist : list of sockets/FDs
sockets/FDs to be polled for error events
Returns
-------
(rlist, wlist, xlist) : tuple of lists of sockets (length 3)
Lists correspond to sockets available for read/write/error events respectively.
"""
    if timeout is None:
        timeout = -1
    # Convert from sec -> us for zmq_poll.
    # zmq_poll accepts 3.x style timeout in ms
    timeout = int(timeout*1000.0)
    if timeout < 0:
        timeout = -1
    sockets = []
    for s in set(rlist + wlist + xlist):
        flags = 0
        if s in rlist:
            flags |= POLLIN
        if s in wlist:
            flags |= POLLOUT
        if s in xlist:
            flags |= POLLERR
        sockets.append((s, flags))
    return_sockets = _poll(sockets, timeout)
    rlist, wlist, xlist = [], [], []
    for s, flags in return_sockets:
        if flags & POLLIN:
            rlist.append(s)
        if flags & POLLOUT:
            wlist.append(s)
        if flags & POLLERR:
            xlist.append(s)
    return rlist, wlist, xlist

#-----------------------------------------------------------------------------
# Symbols to export
#-----------------------------------------------------------------------------

__all__ = [ 'Poller', 'select' ]
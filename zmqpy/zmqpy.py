# coding: utf-8

from ctypes import *
from ctypes.util import find_library

from constants import *
from error import *
from utils import jsonapi

import pickle

czmq = CDLL(find_library("czmq"), use_errno=True)

if not czmq._name:
    raise ImportError('Cannot load czmq library')
    
class _ZMQContext(Structure):
    pass

czmq.zctx_new.restype = POINTER(_ZMQContext)
czmq.zctx_new.argtypes = []

czmq.zctx_destroy.restype = None
czmq.zctx_destroy.argtypes = [c_void_p]

czmq.zctx_set_linger.restype = None
czmq.zctx_set_linger.argtypes = [c_void_p, c_int]

#czmq.zerror_errno.restype = c_int
#czmq.zerror_errno.argtypes = []

czmq.zsocket_new.restype = c_void_p
czmq.zsocket_new.argtypes = [c_void_p, c_int]

czmq.zsocket_destroy.restype = None
czmq.zsocket_destroy.argtypes = [c_void_p, c_void_p]

czmq.zsocket_connect.restype = None
czmq.zsocket_connect.argtypes = [c_void_p, c_char_p]

czmq.zsocket_bind.restype = None
czmq.zsocket_bind.argtypes = [c_void_p, c_char_p]

czmq.zstr_recv.restype = c_char_p
czmq.zstr_recv.argtypes = [c_void_p]

czmq.zstr_send.restype = c_int
czmq.zstr_send.argtypes = [c_void_p, c_char_p]

czmq.zstr_recv_nowait.restype = c_char_p
czmq.zstr_recv_nowait.argtypes = [c_void_p]

'''
//  Receive a string off a socket, caller must free it
char *
    zstr_recv (void *socket);

//  Receive a string off a socket if socket had input waiting
char *
    zstr_recv_nowait (void *socket);

//  Send a string to a socket in ØMQ string format
int
    zstr_send (void *socket, const char *string);

//  Send a string to a socket in ØMQ string format, with MORE flag
int
    zstr_sendm (void *socket, const char *string);

//  Send a formatted string to a socket
int
    zstr_sendf (void *socket, const char *format, ...);
'''

czmq.zsockopt_sndhwm.restype = c_int
czmq.zsockopt_sndhwm.argtypes = [c_void_p]

czmq.zsockopt_rcvhwm.restype = c_int
czmq.zsockopt_rcvhwm.argtypes = [c_void_p]

czmq.zsockopt_affinity.restype = c_int
czmq.zsockopt_affinity.argtypes = [c_void_p]

czmq.zsockopt_rate.restype = c_int
czmq.zsockopt_rate.argtypes = [c_void_p]

czmq.zsockopt_recovery_ivl.restype = c_int
czmq.zsockopt_recovery_ivl.argtypes = [c_void_p]

czmq.zsockopt_sndbuf.restype = c_int
czmq.zsockopt_sndbuf.argtypes = [c_void_p]

czmq.zsockopt_rcvbuf.restype = c_int
czmq.zsockopt_rcvbuf.argtypes = [c_void_p]

czmq.zsockopt_linger.restype = c_int
czmq.zsockopt_linger.argtypes = [c_void_p]

czmq.zsockopt_reconnect_ivl.restype = c_int
czmq.zsockopt_reconnect_ivl.argtypes = [c_void_p]

czmq.zsockopt_reconnect_ivl_max.restype = c_int
czmq.zsockopt_reconnect_ivl_max.argtypes = [c_void_p]

czmq.zsockopt_backlog.restype = c_int
czmq.zsockopt_backlog.argtypes = [c_void_p]

czmq.zsockopt_maxmsgsize.restype = c_int
czmq.zsockopt_maxmsgsize.argtypes = [c_void_p]

czmq.zsockopt_type.restype = c_int
czmq.zsockopt_type.argtypes = [c_void_p]

czmq.zsockopt_rcvmore.restype = c_int
czmq.zsockopt_rcvmore.argtypes = [c_void_p]

czmq.zsockopt_fd.restype = c_int
czmq.zsockopt_fd.argtypes = [c_void_p]

czmq.zsockopt_events.restype = c_int
czmq.zsockopt_events.argtypes = [c_void_p]

czmq.zsockopt_set_sndhwm.restype = None
czmq.zsockopt_set_sndhwm.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_sndhwm.restype = None
czmq.zsockopt_set_sndhwm.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_rcvhwm.restype = None
czmq.zsockopt_set_rcvhwm.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_affinity.restype = None
czmq.zsockopt_set_affinity.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_identity.restype = None
czmq.zsockopt_set_identity.argtypes = [c_void_p, c_char_p]

czmq.zsockopt_set_rate.restype = None
czmq.zsockopt_set_rate.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_recovery_ivl.restype = None
czmq.zsockopt_set_recovery_ivl.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_sndbuf.restype = None
czmq.zsockopt_set_sndbuf.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_linger.restype = None
czmq.zsockopt_set_linger.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_reconnect_ivl.restype = None
czmq.zsockopt_set_reconnect_ivl.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_reconnect_ivl_max.restype = None
czmq.zsockopt_set_reconnect_ivl_max.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_backlog.restype = None
czmq.zsockopt_set_backlog.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_maxmsgsize.restype = None
czmq.zsockopt_set_maxmsgsize.argtypes = [c_void_p, c_int]

czmq.zsockopt_set_subscribe.restype = None
czmq.zsockopt_set_subscribe.argtypes = [c_void_p, c_char_p]

czmq.zsockopt_set_unsubscribe.restype = None
czmq.zsockopt_set_unsubscribe.argtypes = [c_void_p, c_char_p]

class zmq_loop(Structure):
    pass

class zmq_pollitem_t(Structure):
    _fields_ = [("socket", c_void_p),
                ("f", c_int),
                ("events", c_short),
                ("revents", c_short)]

poller_callback_func = CFUNCTYPE(c_void_p, POINTER(zmq_pollitem_t), c_void_p)

czmq.zloop_new.restype = POINTER(zmq_loop)
czmq.zloop_new.argtypes = []

czmq.zloop_destroy.restype = None
czmq.zloop_destroy.argtypes = [POINTER(zmq_loop)]

czmq.zloop_poller.restype = c_int
czmq.zloop_poller.argtypes = [POINTER(zmq_loop), POINTER(zmq_pollitem_t), poller_callback_func, c_void_p]

czmq.zloop_start.restype = c_int
czmq.zloop_start.argtypes = [POINTER(zmq_loop)]

'''
//  Callback function for reactor events
typedef int (zloop_fn) (zloop_t *loop, zmq_pollitem_t *item, void *arg);

//  Create a new zloop reactor
zloop_t *
    zloop_new (void);

//  Destroy a reactor
void
    zloop_destroy (zloop_t **self_p);

//  Register pollitem with the reactor. When the pollitem is ready, will call
//  the handler, passing the arg. Returns 0 if OK, -1 if there was an error.
//  If you register the pollitem more than once, each instance will invoke its
//  corresponding handler.
int
    zloop_poller (zloop_t *self, zmq_pollitem_t *item, zloop_fn handler, void *arg);

//  Cancel a pollitem from the reactor, specified by socket or FD. If both
//  are specified, uses only socket. If multiple poll items exist for same
//  socket/FD, cancels ALL of them.
void
    zloop_poller_end (zloop_t *self, zmq_pollitem_t *item);

//  Register a timer that expires after some delay and repeats some number of
//  times. At each expiry, will call the handler, passing the arg. To
//  run a timer forever, use 0 times. Returns 0 if OK, -1 if there was an
//  error.
int
    zloop_timer (zloop_t *self, size_t delay, size_t times, zloop_fn handler, void *arg);

//  Cancel all timers for a specific argument (as provided in zloop_timer)
void
    zloop_timer_end (zloop_t *self, void *arg);

//  Set verbose tracing of reactor on/off
void
    zloop_set_verbose (zloop_t *self, Bool verbose);

//  Start the reactor. Takes control of the thread and returns when the ØMQ
//  context is terminated or the process is interrupted, or any event handler
//  returns -1. Event handlers may register new sockets and timers, and
//  cancel sockets. Returns 0 if interrupted, -1 if cancelled by a handler.
int
    zloop_start (zloop_t *self);
'''


_instance = None

class Context(object):
    def __init__(self, io_threads=1):
        if not io_threads > 0:
            raise ZMQError(EINVAL)
        self.ctx = czmq.zctx_new()
        czmq.zctx_set_linger(self.ctx, c_int(1))
        self._closed = False
        self.n_sockets = 0
        self.max_sockets = 32
        self._sockets = {}
        
    def term(self):
        for k, s in self._sockets.items():
            if not s.closed:
                s.close()
        czmq.zctx_destroy(pointer(self.ctx))
        self._closed = True

    @property
    def closed(self):
        return self._closed

    @classmethod
    def instance(cls, io_threads=1):
        global _instance
        if _instance is None or _instance.closed:
            _instance = cls(io_threads)
        return _instance

    def _add_socket(self, socket):
        self._sockets[self.n_sockets] = socket
        self.n_sockets += 1
        return self.n_sockets
        
    def _rm_socket(self, n):
        del self._sockets[n]
        
    def socket(self, sock_type):
        if self._closed:
            raise ZMQError(ENOTSUP)
        return Socket(self, sock_type)
        

class Socket(object):
    def __init__(self, context, sock_type):
        self.context = context
        self.sock_type = sock_type
        self.handle = czmq.zsocket_new(self.context.ctx, c_int(self.sock_type))
        if not self.handle:
            raise ZMQError()
        self._closed = False
        self._attrs = {}
        self.n = self.context._add_socket(self)
       
    @property 
    def closed(self):
        return self._closed

    def setsockopt(self, option, _type):
        if option == LINGER:
            czmq.zsockopt_set_linger(self.handle, c_int(_type))
        if option == SUBSCRIBE:
            czmq.zsockopt_set_subscribe(self.handle, c_char_p(_type))
    
    def bind(self, address):
        czmq.zsocket_bind(self.handle, c_char_p(address))

    def connect(self, address):
	czmq.zsocket_connect(self.handle, c_char_p(address))

    def send(self, content, flags=0, copy=True, track=False):
        czmq.zstr_send(self.handle, c_char_p(content))
    
    def recv(self, flags=0, copy=True, track=False):
        if flags == DONTWAIT:
            data = czmq.zstr_recv_nowait(self.handle)
            if not data:
                raise zmqpy.ZMQError()
            
        return czmq.zstr_recv(self.handle)
        
    def send_pyobj(self, obj, flags=0, protocol=0):
        """s.send_pyobj(obj, flags=0, protocol=0)

        Send a Python object as a message using pickle to serialize.

        Parameters
        ----------
        obj : Python object
            The Python object to send.
        flags : int
            Any valid send flag.
        protocol : int
            The pickle protocol number to use. Default of -1 will select
            the highest supported number. Use 0 for multiple platform
            support.
        """
        msg = pickle.dumps(obj, protocol)
        return self.send(msg, flags)

    def recv_pyobj(self, flags=0):
        """s.recv_pyobj(flags=0)

        Receive a Python object as a message using pickle to serialize.

        Parameters
        ----------
        flags : int
            Any valid recv flag.

        Returns
        -------
        obj : Python object
            The Python object that arrives as a message.
        """
        s = self.recv(flags)
        return pickle.loads(s)

    def send_json(self, obj, flags=0):
        """s.send_json(obj, flags=0)

        Send a Python object as a message using json to serialize.

        Parameters
        ----------
        obj : Python object
            The Python object to send.
        flags : int
            Any valid send flag.
        """
        if jsonapi.jsonmod is None:
            raise ImportError('jsonlib{1,2}, json or simplejson library is \
                               required.')
        else:
            msg = jsonapi.dumps(obj)
            return self.send(msg, flags)

    def recv_json(self, flags=0):
        """s.recv_json(flags=0)

        Receive a Python object as a message using json to serialize.

        Parameters
        ----------
        flags : int
            Any valid recv flag.

        Returns
        -------
        obj : Python object
            The Python object that arrives as a message.
        """
        if jsonapi.jsonmod is None:
            raise ImportError('jsonlib{1,2}, json or simplejson library is re \
                               quired.')
        else:
            msg = self.recv(flags)
            return jsonapi.loads(msg)     
        
        
    def close(self):
        if not self._closed:
            czmq.zsocket_destroy(self.context.ctx, self.handle)
            self._closed = True

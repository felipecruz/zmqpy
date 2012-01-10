# coding: utf-8

from ctypes import *
from ctypes.util import find_library

from constants import *
from error import *
from utils import jsonapi

from collections import defaultdict

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

czmq.zctx_set_iothreads.restype = None
czmq.zctx_set_iothreads.argtypes = [c_void_p, c_int]

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

poller_callback_func = CFUNCTYPE(c_int, 
                                 POINTER(zmq_loop), 
                                 POINTER(zmq_pollitem_t), 
                                 c_void_p)

czmq.zloop_new.restype = POINTER(zmq_loop)
czmq.zloop_new.argtypes = []

czmq.zloop_destroy.restype = None
czmq.zloop_destroy.argtypes = [POINTER(POINTER(zmq_loop))]

czmq.zloop_poller.restype = c_int
czmq.zloop_poller.argtypes = [
        POINTER(zmq_loop), 
        POINTER(zmq_pollitem_t), 
        poller_callback_func, 
        c_void_p
    ]

czmq.zloop_poller_end.restype = None
czmq.zloop_poller_end.argtypes = [POINTER(zmq_loop), POINTER(zmq_pollitem_t)]

czmq.zloop_start.restype = c_int
czmq.zloop_start.argtypes = [POINTER(zmq_loop)]

czmq.zloop_timer.restype = c_int
czmq.zloop_timer.argtypes = [
                                POINTER(zmq_loop), 
                                c_size_t, 
                                c_size_t, 
                                poller_callback_func, 
                                c_void_p
                            ]

czmq.zloop_set_verbose.restype = None
czmq.zloop_set_verbose.argtypes = [POINTER(zmq_loop), c_bool]

class Loop(object):
    def __init__(self, verbose=False):
        self.loop = czmq.zloop_new()
        if verbose:
            czmq.zloop_set_verbose(self.loop, c_bool(True))
        #self.callbacks = defaultdict(list)

    def start(self):
        rc = czmq.zloop_start(self.loop)
        return rc
    
    def timer(self, delay, times, function, socket):
        czmq.zloop_timer(self.loop, 
                         c_size_t(delay), 
                         c_size_t(times),
                         poller_callback_func(function),
                         c_void_p(socket.handle)
                         )
         

    def poller(self, item, event, socket):
        socket_handler = socket
        if hasattr(socket, 'handle'):
            socket_handler = socket.handle

        #self.callbacks[item].append(event)
        czmq.zloop_poller(self.loop,
                          pointer(item),
                          poller_callback_func(event),
                          socket_handler
                          )

    def poller_end(self, item):
        #del self.callbacks[item]
        czmq.zloop_poller_end(self.loop,
                              pointer(item)
                             )

    def destroy(self):
        czmq.zloop_destroy(pointer(self.loop))

_instance = None

class Context(object):
    def __init__(self, iothreads=1):
        if not iothreads > 0:
            raise ZMQError(EINVAL)
        self.ctx = czmq.zctx_new()
        self.linger = 1
        self.iothreads = iothreads
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
    def instance(cls, iothreads=1):
        global _instance
        if _instance is None or _instance.closed:
            _instance = cls(iothreads)
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

    def set_iothreads(self, iothreads=1):
        czmq.zctx_set_iothreads(self.ctx, c_int(iothreads))
        self.iothreads = iothreads

    def set_linger(self, linger=1):
        czmq.zctx_set_linger(self.ctx, c_int(linger))
        self.linger = linger

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
            return data

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

'''
//  Create a new frame with optional size, and optional data
zframe_t *
    zframe_new (const void *data, size_t size);

//  Destroy a frame
void
    zframe_destroy (zframe_t **self_p);

//  Receive frame from socket, returns zframe_t object or NULL if the recv
//  was interrupted. Does a blocking recv, if you want to not block then use
//  zframe_recv_nowait().
zframe_t *
    zframe_recv (void *socket);

//  Receive a new frame off the socket. Returns newly allocated frame, or
//  NULL if there was no input waiting, or if the read was interrupted.
zframe_t *
    zframe_recv_nowait (void *socket);

    //  Send a frame to a socket, destroy frame after sending
void
    zframe_send (zframe_t **self_p, void *socket, int flags);

'''
class zmq_msg_t(Structure):
    __fields__ = ('_',c_ubyte * 32)

class zmq_frame(Structure):
    __fields__ = [
                    ('zmsg', zmq_msg_t),
                    ('more', c_int)
                ]

czmq.zframe_new.restype = POINTER(zmq_frame)
czmq.zframe_new.argtypes = [c_void_p, c_size_t]

czmq.zframe_recv.restype = POINTER(zmq_frame)
czmq.zframe_recv.argtypes = [c_void_p]

czmq.zframe_recv_nowait.restype = POINTER(zmq_frame)
czmq.zframe_recv_nowait.argtypes = [c_void_p]

czmq.zframe_send.restype = c_int
czmq.zframe_send.argtypes = [POINTER(POINTER(zmq_frame)), c_void_p, c_int]

czmq.zframe_data.restype = c_char_p
czmq.zframe_data.argtypes = [POINTER(zmq_frame)]

class ZFrame(object):
    '''
        zmq frame object
    '''
    def __init__(self, data=None):
        self.data = data
        if data:
            buffer = create_string_buffer(data)
            self.zframe = czmq.zframe_new(
                            buffer,
                            c_size_t(sizeof(buffer))
                            )
        else:
            self.zframe = czmq.zframe_new(
                            POINTER(c_int)(),
                            c_ulong(0)
                        )

    def send(self, socket, flags):
        return czmq.zframe_send(
                pointer(self.zframe),
                socket.handle,
                c_int(flags)
            )

    @staticmethod
    def recv(socket):
        frame_ref = czmq.zframe_recv(socket.handle)
        str_data = czmq.zframe_data(frame_ref)
        return ZFrame(str_data)

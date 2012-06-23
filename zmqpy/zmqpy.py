# coding: utf-8

import cPickle as pickle
from ctypes import *

from _ctypes import *
from constants import *
from error import *
from utils import jsonapi

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
            czmq.zsocket_set_linger(self.handle, c_int(_type))
        if option == SUBSCRIBE:
            czmq.zsocket_set_subscribe(self.handle, c_char_p(_type))
        if option == IDENTITY:
            czmq.zsocket_set_identity(self.handle, c_char_p(_type))

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
                         c_void_p(socket.handle))

    def poller(self, item, event, socket):
        socket_handler = socket
        if hasattr(socket, 'handle'):
            socket_handler = socket.handle

        #self.callbacks[item].append(event)
        czmq.zloop_poller(self.loop,
                          pointer(item),
                          poller_callback_func(event),
                          socket_handler)

    def poller_end(self, item):
        #del self.callbacks[item]
        czmq.zloop_poller_end(self.loop,
                              pointer(item))

    def destroy(self):
        czmq.zloop_destroy(pointer(self.loop))

class ZFrame(object):
    '''
        zmq frame object
    '''
    def __init__(self, data=None):
        self._data = data
        if data:
            buffer = create_string_buffer(data)
            self.zframe = czmq.zframe_new(buffer,
                                          c_size_t(sizeof(buffer)))
        else:
            self.zframe = czmq.zframe_new(POINTER(c_int)(),
                                          c_ulong(0))

    def send(self, socket, flags):
        return czmq.zframe_send(pointer(self.zframe),
                                socket.handle,
                                c_int(flags))

    @property
    def data(self):
        return self._data

    @staticmethod
    def recv(socket):
        frame_ref = czmq.zframe_recv(socket.handle)
        str_data = czmq.zframe_data(frame_ref)
        return ZFrame(str_data)

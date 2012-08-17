# coding: utf-8

#import cPickle as pickle
#from ctypes import *
#from _ctypes import *

from _cffi import C, ffi
from constants import *
from error import *
from utils import jsonapi

class Context(object):
    _state = {}
    def __init__(self, iothreads=1):
        if not iothreads > 0:
            raise ZMQError(EINVAL)

        self.__dict__ = self._state

        self.zmq_ctx = C.zmq_init(iothreads)
        self.iothreads = iothreads
        self._closed = False
        self.n_sockets = 0
        self.max_sockets = 32
        self._sockets = {}
        self.sockopts = {LINGER: 1}
        self.linger = 1

    def term(self):
        if self.closed:
            return

        for k, s in self._sockets.items():
            if not s.closed:
                s.close()
            del self._sockets[k]

        C.zmq_term(self.zmq_ctx)
        self.zmq_ctx = None
        self._closed = True
        self.n_sockets = 0

    @property
    def closed(self):
        return self._closed

    def _add_socket(self, socket):
        self._sockets[self.n_sockets] = socket
        self.n_sockets += 1

        return self.n_sockets

    def _rm_socket(self, n):
        del self._sockets[n]

    def socket(self, sock_type):
        if self._closed:
            raise ZMQError(ENOTSUP)

        socket = Socket(self, sock_type)
        for option, option_value in self.sockopts.items():
            socket.setsockopt(option, option_value)

        return socket

    def set_linger(self, value):
        self.sockopts[LINGER] = value
        self.linger = value

class Socket(object):
    def __init__(self, context, sock_type):
        self.context = context
        self.sock_type = sock_type
        self.zmq_socket = C.zmq_socket(context.zmq_ctx, sock_type)
        if not self.zmq_socket:
            raise ZMQError()
        self._closed = False
        self._attrs = {}
        self.n = self.context._add_socket(self)
        self.last_errno = None

    @property
    def closed(self):
        return self._closed

    def close(self):
        if not self._closed:
            C.zmq_close(self.zmq_socket)
            self._closed = True

    def bind(self, address):
        ret = C.zmq_bind(self.zmq_socket, address)
        return ret

    def connect(self, address):
        ret = C.zmq_connect(self.zmq_socket, address)
        return ret

    def setsockopt(self, option, value):
        if isinstance(value, str):
            c_val = ffi.new('char[]', value)
            ret = C.zmq_setsockopt(self.zmq_socket,
                                   option,
                                   ffi.cast('void*', c_val),
                                   len(value))
        elif isinstance(value, int):
            c_val = ffi.new('int*', value)
            ret = C.zmq_setsockopt(self.zmq_socket,
                                   option,
                                   ffi.cast('void*', c_val),
                                   ffi.sizeof('int'))
        else:
            raise ZMQError("Invalid option value")

    def send(self, message, flags=0, copy=False):
        zmq_msg = ffi.new('zmq_msg_t*')

        c_message = ffi.new('char[%d]' % len(message), message)
        C.zmq_msg_init_data(zmq_msg, ffi.cast('void*', c_message),
                                     ffi.cast('size_t', len(message)),
                                     ffi.NULL,
                                     ffi.NULL)

        ret = C.zmq_send(self.zmq_socket, zmq_msg, flags)
        C.zmq_msg_close(zmq_msg)
        if ret < 0:
            self.last_errno = C.zmq_errno()

        return ret

    def recv(self, flags=0):
        zmq_msg = ffi.new('zmq_msg_t*')
        C.zmq_msg_init(zmq_msg)

        ret = C.zmq_recv(self.zmq_socket, zmq_msg, flags)
        if ret < 0:
            C.zmq_msg_close(zmq_msg)
            raise zmqpy.ZMQError(_errno=C.zmq_errno())

        value = ffi.buffer(C.zmq_msg_data(zmq_msg), int(C.zmq_msg_size(zmq_msg)))[:]

        C.zmq_msg_close(zmq_msg)

        return value

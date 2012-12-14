# coding: utf-8

from ._cffi import C, ffi, zmq_version, new_uint64_pointer, \
                                        new_int64_pointer, \
                                        new_int_pointer, \
                                        new_binary_data, \
                                        value_uint64_pointer, \
                                        value_int64_pointer, \
                                        value_int_pointer, \
                                        value_binary_data

from .constants import *
from .error import *
from .utils import jsonapi

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

def new_pointer_from_opt(option, length=0):
    if option in uint64_opts:
        return new_uint64_pointer()
    elif option in int64_opts:
        return new_int64_pointer()
    elif option in int_opts:
        return new_int_pointer()
    elif option in binary_opts:
        return new_binary_data(length)
    else:
        raise ValueError('Invalid option')

def value_from_opt_pointer(option, opt_pointer, length=0):
    if option in uint64_opts:
        return int(opt_pointer[0])
    elif option in int64_opts:
        return int(opt_pointer[0])
    elif option in int_opts:
        return int(opt_pointer[0])
    elif option in binary_opts:
        return ffi.string(opt_pointer)
    else:
        raise ValueError('Invalid option')

def initialize_opt_pointer(option, value, length=0):
    if option in uint64_opts:
        return value_uint64_pointer(value)
    elif option in int64_opts:
        return value_int64_pointer(value)
    elif option in int_opts:
        return value_int_pointer(value)
    elif option in binary_opts:
        return value_binary_data(value, length)
    else:
        raise ValueError('Invalid option')

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
        length = None
        if isinstance(value, str):
            length = len(value)
        low_level_data = initialize_opt_pointer(option, value, length)
        low_level_value_pointer = low_level_data[0]
        low_level_sizet = low_level_data[1]
        ret = C.zmq_setsockopt(self.zmq_socket,
                                option,
                                ffi.cast('void*', low_level_value_pointer),
                                low_level_sizet)
        return ret

    def getsockopt(self, option, length=0):
        low_level_data = new_pointer_from_opt(option, length=length)
        low_level_value_pointer = low_level_data[0]
        low_level_sizet_pointer = low_level_data[1]

        ret = C.zmq_getsockopt(self.zmq_socket,
                               option,
                               low_level_value_pointer,
                               low_level_sizet_pointer)

        if ret < 0:
            self.last_errno = C.zmq_errno()
            return -1

        return value_from_opt_pointer(option, low_level_value_pointer)

    def send(self, message, flags=0, copy=False, track=False):
        zmq_msg = ffi.new('zmq_msg_t*')

        c_message = ffi.new('char[]', message)
        C.zmq_msg_init_size(zmq_msg, len(message))
        C.memcpy(C.zmq_msg_data(zmq_msg), c_message, len(message))

        if zmq_version == 2:
            ret = C.zmq_send(self.zmq_socket, zmq_msg, flags)
        else:
            ret = C.zmq_sendmsg(self. zmq_socket, zmq_msg, flags)

        C.zmq_msg_close(zmq_msg)
        if ret < 0:
            self.last_errno = C.zmq_errno()

        return ret

    def recv(self, flags=0, copy=False, track=False):
        zmq_msg = ffi.new('zmq_msg_t*')
        C.zmq_msg_init(zmq_msg)

        if zmq_version == 2:
            ret = C.zmq_recv(self.zmq_socket, zmq_msg, flags)
        else:
            ret = C.zmq_recvmsg(self.zmq_socket, zmq_msg, flags)

        if ret < 0:
            C.zmq_msg_close(zmq_msg)
            raise zmqpy.ZMQError(_errno=C.zmq_errno())

        value = ffi.buffer(C.zmq_msg_data(zmq_msg), int(C.zmq_msg_size(zmq_msg)))[:]

        C.zmq_msg_close(zmq_msg)

        return value

    # Following methods from pyzmq.pysocket

    def bind_to_random_port(self, addr, min_port=49152, max_port=65536, max_tries=100):
        """s.bind_to_random_port(addr, min_port=49152, max_port=65536, max_tries=100)

        Bind this socket to a random port in a range.

        Parameters
        ----------
        addr : str
            The address string without the port to pass to ``Socket.bind()``.
        min_port : int, optional
            The minimum port in the range of ports to try (inclusive).
        max_port : int, optional
            The maximum port in the range of ports to try (exclusive).
        max_tries : int, optional
            The maximum number of bind attempts to make.

        Returns
        -------
        port : int
            The port the socket was bound to.

        Raises
        ------
        ZMQBindError
            if `max_tries` reached before successful bind
        """
        for i in range(max_tries):
            try:
                port = random.randrange(min_port, max_port)
                self.bind('%s:%s' % (addr, port))
            except ZMQError as exception:
                if not exception.errno == zmq.EADDRINUSE:
                    raise
            else:
                return port
        raise ZMQBindError("Could not bind socket to random port.")

    def send_multipart(self, msg_parts, flags=0, copy=True, track=False):
        """s.send_multipart(msg_parts, flags=0, copy=True, track=False)

        Send a sequence of buffers as a multipart message.

        Parameters
        ----------
        msg_parts : iterable
            A sequence of objects to send as a multipart message. Each element
            can be any sendable object (Frame, bytes, buffer-providers)
        flags : int, optional
            SNDMORE is handled automatically for frames before the last.
        copy : bool, optional
            Should the frame(s) be sent in a copying or non-copying manner.
        track : bool, optional
            Should the frame(s) be tracked for notification that ZMQ has
            finished with it (ignored if copy=True).

        Returns
        -------
        None : if copy or not track
        MessageTracker : if track and not copy
            a MessageTracker object, whose `pending` property will
            be True until the last send is completed.
        """
        for msg in msg_parts[:-1]:
            self.send(msg, SNDMORE|flags, copy=copy, track=track)
        # Send the last part without the extra SNDMORE flag.
        return self.send(msg_parts[-1], flags, copy=copy, track=track)

    def recv_multipart(self, flags=0, copy=True, track=False):
        """s.recv_multipart(flags=0, copy=True, track=False)

        Receive a multipart message as a list of bytes or Frame objects.

        Parameters
        ----------
        flags : int, optional
            Any supported flag: NOBLOCK. If NOBLOCK is set, this method
            will raise a ZMQError with EAGAIN if a message is not ready.
            If NOBLOCK is not set, then this method will block until a
            message arrives.
        copy : bool, optional
            Should the message frame(s) be received in a copying or non-copying manner?
            If False a Frame object is returned for each part, if True a copy of
            the bytes is made for each frame.
        track : bool, optional
            Should the message frame(s) be tracked for notification that ZMQ has
            finished with it? (ignored if copy=True)
        Returns
        -------
        msg_parts : list
            A list of frames in the multipart message; either Frames or bytes,
            depending on `copy`.

        """
        parts = [self.recv(flags, copy=copy, track=track)]
        # have first part already, only loop while more to receive
        while self.getsockopt(RCVMORE):
            part = self.recv(flags, copy=copy, track=track)
            parts.append(part)

        return parts

def _make_zmq_pollitem(socket, flags):
    zmq_socket = socket.zmq_socket
    zmq_pollitem = ffi.new('zmq_pollitem_t*')
    zmq_pollitem.socket = zmq_socket
    zmq_pollitem.fd = 0
    zmq_pollitem.events = flags
    zmq_pollitem.revents = 0
    return zmq_pollitem[0]

def _make_zmq_pollitem_fromfd(socket_fd, flags):
    zmq_pollitem = ffi.new('zmq_pollitem_t*')
    zmq_pollitem.socket = ffi.NULL
    zmq_pollitem.fd = socket_fd
    zmq_pollitem.events = flags
    zmq_pollitem.revents = 0
    return zmq_pollitem[0]

def _cffi_poll(zmq_pollitem_list, poller, timeout=-1):
    if zmq_version == 2:
        timeout = timeout * 1000
    items = ffi.new('zmq_pollitem_t[]', zmq_pollitem_list)
    list_length = ffi.cast('int', len(zmq_pollitem_list))
    c_timeout = ffi.cast('long', timeout)
    C.zmq_poll(items, list_length, c_timeout)
    result = []
    for index in range(len(items)):
        if items[index].revents > 0:
            if not items[index].socket == ffi.NULL:
                result.append((poller._sockets[items[index].socket],
                            items[index].revents))
            else:
                result.append((items[index].fd, items[index].revents))
    return result

def _poll(sockets, timeout):
    cffi_pollitem_list = []
    low_level_to_socket_obj = {}
    for item in sockets:
        low_level_to_socket_obj[item[0].zmq_socket] = item
        cffi_pollitem_list.append(_make_zmq_pollitem(item[0], item[1]))
    items = ffi.new('zmq_pollitem_t[]', cffi_pollitem_list)
    list_length = ffi.cast('int', len(cffi_pollitem_list))
    c_timeout = ffi.cast('long', timeout)
    C.zmq_poll(items, list_length, c_timeout)
    result = []
    for index in range(len(items)):
        if items[index].revents > 0:
            result.append((low_level_to_socket_obj[items[index].socket][0],
                           items[index].revents))
    return result

class Poller(object):
    def __init__(self):
        self.sockets_flags = {}
        self._sockets = {}
        self.c_sockets = {}

    @property
    def sockets(self):
        return self.sockets_flags

    def register(self, socket, flags=POLLIN|POLLOUT):
        if flags:
            self.sockets_flags[socket] = flags
            if isinstance(socket, int):
                self.c_sockets[socket] = _make_zmq_pollitem_fromfd(socket, flags)
            else:
                self.c_sockets[socket] =  _make_zmq_pollitem(socket, flags)
                self._sockets[socket.zmq_socket] = socket
        elif socket in self.sockets_flags:
            # uregister sockets registered with no events
            self.unregister(socket)
        else:
            # ignore new sockets with no events
            pass

    def modify(self, socket, flags=POLLIN|POLLOUT):
        self.register(socket, flags)

    def unregister(self, socket):
        del self.sockets_flags[socket]
        del self.c_sockets[socket]

        if not isinstance(socket, int):
            del self._sockets[socket.zmq_socket]

    def poll(self, timeout=None):
        if timeout is None:
            timeout = -1

        timeout = int(timeout)
        if timeout < 0:
            timeout = -1

        items =  _cffi_poll(self.c_sockets.values(),
                            self,
                            timeout=timeout)

        return items

def select(rlist, wlist, xlist, timeout=None):
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

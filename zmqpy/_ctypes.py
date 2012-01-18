# coding: utf-8

from ctypes import *
from ctypes.util import find_library

from constants import *
from error import *

#FIXME check version!!
zmq_version_major = 2

czmq = CDLL(find_library("czmq"), use_errno=True)

if not czmq._name:
    raise ImportError('Cannot load czmq library')
    
class zmq_context(Structure):
    pass

class zmq_loop(Structure):
    pass

class zmq_pollitem_t(Structure):
    _fields_ = [("socket", c_void_p),
                ("f", c_int),
                ("events", c_short),
                ("revents", c_short)]

class zmq_msg_t(Structure):
    __fields__ = ('_',c_ubyte * 32)

class zmq_frame(Structure):
    __fields__ = [
                    ('zmsg', zmq_msg_t),
                    ('more', c_int)
                 ]

czmq.zctx_new.restype = POINTER(zmq_context)
czmq.zctx_new.argtypes = []

czmq.zctx_destroy.restype = None
czmq.zctx_destroy.argtypes = [c_void_p]

czmq.zctx_set_linger.restype = None
czmq.zctx_set_linger.argtypes = [c_void_p, c_int]

czmq.zctx_set_iothreads.restype = None
czmq.zctx_set_iothreads.argtypes = [c_void_p, c_int]

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

if zmq_version_major == 2:
    czmq.zsockopt_hwm.restype = c_int
    czmq.zsockopt_hwm.argtypes = [c_void_p]

    czmq.zsockopt_swap.restype = c_int
    czmq.zsockopt_swap.argtypes = [c_void_p]

    czmq.zsockopt_affinity.restype = c_int
    czmq.zsockopt_affinity.argtypes = [c_void_p]

    czmq.zsockopt_rate.restype = c_int
    czmq.zsockopt_rate.argtypes = [c_void_p]

    czmq.zsockopt_recovery_ivl.restype = c_int
    czmq.zsockopt_recovery_ivl.argtypes = [c_void_p]

    czmq.zsockopt_recovery_ivl_msec.restype = c_int
    czmq.zsockopt_recovery_ivl_msec.argtypes = [c_void_p]

    czmq.zsockopt_mcast_loop.restype = c_int
    czmq.zsockopt_mcast_loop.argtypes = [c_void_p]

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

    czmq.zsockopt_type.restype = c_int
    czmq.zsockopt_type.argtypes = [c_void_p]

    czmq.zsockopt_rcvmore.restype = c_int
    czmq.zsockopt_rcvmore.argtypes = [c_void_p]

    czmq.zsockopt_fd.restype = c_int
    czmq.zsockopt_fd.argtypes = [c_void_p]

    czmq.zsockopt_events.restype = c_int
    czmq.zsockopt_events.argtypes = [c_void_p]

    czmq.zsockopt_set_hwm.restype = None
    czmq.zsockopt_set_hwm.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_swap.restype = None
    czmq.zsockopt_set_swap.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_affinity.restype = None
    czmq.zsockopt_set_affinity.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_identity.restype = None
    czmq.zsockopt_set_identity.argtypes = [c_void_p, c_char_p]
    
    czmq.zsockopt_set_rate.restype = None
    czmq.zsockopt_set_rate.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_recovery_ivl.restype = None
    czmq.zsockopt_set_recovery_ivl.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_recovery_ivl_msec.restype = None
    czmq.zsockopt_set_recovery_ivl_msec.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_mcast_loop.restype = None
    czmq.zsockopt_set_mcast_loop.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_sndbuf.restype = None
    czmq.zsockopt_set_sndbuf.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_rcvbuf.restype = None
    czmq.zsockopt_set_rcvbuf.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_linger.restype = None
    czmq.zsockopt_set_linger.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_reconnect_ivl.restype = None
    czmq.zsockopt_set_reconnect_ivl.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_reconnect_ivl_max.restype = None
    czmq.zsockopt_set_reconnect_ivl_max.argtypes = [c_void_p, c_int]
    
    czmq.zsockopt_set_backlog.restype = None
    czmq.zsockopt_set_backlog.argtypes = [c_void_p, c_int]

    czmq.zsockopt_set_subscribe.restype = None
    czmq.zsockopt_set_subscribe.argtypes = [c_void_p, c_char_p]
    
    czmq.zsockopt_set_unsubscribe.restype = None
    czmq.zsockopt_set_unsubscribe.argtypes = [c_void_p, c_char_p]


if zmq_version_major == 3:
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

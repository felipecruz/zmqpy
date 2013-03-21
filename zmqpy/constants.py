# coding: utf-8

from ._cffi import C, constant_names, zmq_version

names = None
pynames = []

_constants = {}

for cname in constant_names:
    pyname = cname.split('_', 1)[-1]
    pynames.append(pyname)
    _constants[pyname] = getattr(C, cname)

globals().update(_constants)

if zmq_version == 2:
    DONTWAIT = NOBLOCK
    pynames.append('DONTWAIT')
    globals()['DONTWAIT'] = DONTWAIT
else:
    NOBLOCK = DONTWAIT
    pynames.append('NOBLOCK')
    globals()['NOBLOCK'] = NOBLOCK

uint64_opts = int64_opts = binary_opts = int_opts = []

if zmq_version == 2:
    uint64_opts = [HWM, AFFINITY, SNDBUF, RCVBUF]

    int64_opts =  [SWAP, RECOVERY_IVL, RECOVERY_IVL_MSEC,
                   MCAST_LOOP, RATE, RCVMORE]

    binary_opts = [IDENTITY, SUBSCRIBE, UNSUBSCRIBE]

    int_opts =    [RCVTIMEO, SNDTIMEO, LINGER, RECONNECT_IVL,
                   RECONNECT_IVL_MAX, BACKLOG, FD, EVENTS, TYPE]

    DONTWAIT = NOBLOCK
else:
    uint64_opts = [AFFINITY, SNDBUF, RCVBUF]

    int64_opts =  [RECOVERY_IVL]

    binary_opts = [IDENTITY, SUBSCRIBE, UNSUBSCRIBE]

    int_opts =    [RCVHWM, SNDHWM, RCVTIMEO, SNDTIMEO,
                   LINGER, RECONNECT_IVL, RECONNECT_IVL_MAX,
                   BACKLOG, RATE, RCVMORE, FD, EVENTS, TYPE]

    NOBLOCK = DONTWAIT

# compatibility with default core constants

int_sockopts = []
int_sockopts.extend(int_opts)

int64_sockopts = []
int64_sockopts.extend(int64_opts)
int64_sockopts.extend(uint64_opts)

bytes_sockopts = []
bytes_sockopts.extend(binary_opts)

pynames.extend([
    'binary_opts',
    'int_opts',
    'int64_opts',
    'uint64_opts',
    'bytes_sockopts',
])

__all__ = pynames

import pytest

def test_zmq_init():
    from zmqpy._cffi import C

    ctx = C.zmq_init(1)

    assert ctx

def test_zmq_term():
    from zmqpy._cffi import C

    ctx = C.zmq_init(1)
    ret = C.zmq_term(ctx)

    assert ret == 0

def test_zmq_socket():
    from zmqpy._cffi import C
    from zmqpy.constants import PUSH

    ctx = C.zmq_init(1)
    socket = C.zmq_socket(ctx, PUSH)

    assert socket

def test_zmq_socket_close():
    from zmqpy._cffi import C
    from zmqpy.constants import PUSH

    ctx = C.zmq_init(1)
    socket = C.zmq_socket(ctx, PUSH)

    ret = C.zmq_close(socket)

    assert ret == 0

def test_zmq_setsockopt():
    from zmqpy._cffi import C, ffi
    from zmqpy.constants import PUSH, IDENTITY

    ctx = C.zmq_init(1)
    socket = C.zmq_socket(ctx, PUSH)

    identity = ffi.new('char[3]', 'zmq')
    ret = C.zmq_setsockopt(socket, IDENTITY, ffi.cast('void*', identity), 3)
    assert ret == 0


def test_zmq_bind_connect():
    from zmqpy.constants import PAIR

    ctx = C.zmq_init(1)
    socket1 = C.zmq_socket(ctx, PAIR)
    r1 = C.zmq_bind(socket1, 'tcp://*:5555')

    assert r1 == 0

def test_zmq_bind_connect():
    from zmqpy._cffi import C, ffi
    from zmqpy.constants import PAIR

    ctx = C.zmq_init(1)

    socket1 = C.zmq_socket(ctx, PAIR)
    socket2 = C.zmq_socket(ctx, PAIR)

    r1 = C.zmq_bind(socket1, 'tcp://*:5555')
    r2 = C.zmq_connect(socket2, 'tcp://127.0.0.1:5555')

    assert r1 == 0
    assert r2 == 0

def test_zmq_msg_init():
    from zmqpy._cffi import C, ffi

    zmq_msg = ffi.new('zmq_msg_t')

    assert zmq_msg

    C.zmq_msg_init(zmq_msg)

    assert zmq_msg

def test_zmq_msg_close():
    from zmqpy._cffi import C, ffi

    zmq_msg = ffi.new('zmq_msg_t')
    C.zmq_msg_init(zmq_msg)
    ret = C.zmq_msg_close(zmq_msg)

    assert ret == 0

def test_zmq_msg_init_size():
    from zmqpy._cffi import C, ffi

    zmq_msg = ffi.new('zmq_msg_t')

    assert zmq_msg

    C.zmq_msg_init_size(zmq_msg, 10)

    assert zmq_msg

def test_zmq_msg_init_data():
    from zmqpy._cffi import C, ffi

    zmq_msg = ffi.new('zmq_msg_t')
    assert zmq_msg

    message = ffi.new('char[5]', 'Hello')
    C.zmq_msg_init_data(zmq_msg, ffi.cast('void*', message), 5, ffi.NULL,
                                                                ffi.NULL)

    assert zmq_msg

def test_zmq_msg_close():
    from zmqpy._cffi import C, ffi

    zmq_msg = ffi.new('zmq_msg_t')
    assert zmq_msg

    message = ffi.new('char[5]', 'Hello')
    C.zmq_msg_init_data(zmq_msg, ffi.cast('void*', message), 5, ffi.NULL,
                                                                ffi.NULL)

    assert zmq_msg

    ret = C.zmq_msg_close(zmq_msg)
    assert ret == 0

def test_zmq_msg_data():
    from zmqpy._cffi import C, ffi

    zmq_msg = ffi.new('zmq_msg_t')
    assert zmq_msg

    message = ffi.new('char[]', 'Hello')
    C.zmq_msg_init_data(zmq_msg, ffi.cast('void*', message), 5, ffi.NULL,
                                                                ffi.NULL)

    assert zmq_msg

    data = C.zmq_msg_data(zmq_msg)
    assert str(ffi.cast("char*", data)) == 'Hello'


def test_zmq_send():
    from zmqpy.constants import PAIR, NOBLOCK
    from zmqpy._cffi import C, ffi

    zmq_msg = ffi.new('zmq_msg_t')

    message = ffi.new('char[5]', 'Hello')
    C.zmq_msg_init_data(zmq_msg, ffi.cast('void*', message), 5, ffi.NULL,
                                                                ffi.NULL)

    ctx = C.zmq_init(1)

    socket1 = C.zmq_socket(ctx, PAIR)
    socket2 = C.zmq_socket(ctx, PAIR)

    r1 = C.zmq_bind(socket1, 'tcp://*:5555')
    r2 = C.zmq_connect(socket2, 'tcp://127.0.0.1:5555')

    ret = C.zmq_send(socket2, zmq_msg, 0)
    assert ret == 0

def test_zmq_recv():
    from zmqpy.constants import REQ, REP, NOBLOCK
    from zmqpy._cffi import C, ffi

    ctx = C.zmq_init(1)

    sender = C.zmq_socket(ctx, REQ)
    receiver = C.zmq_socket(ctx, REP)

    r1 = C.zmq_bind(receiver, 'tcp://*:3333')
    r2 = C.zmq_connect(sender, 'tcp://127.0.0.1:3333')

    zmq_msg = ffi.new('zmq_msg_t')
    message = ffi.new('char[5]', 'Hello')

    C.zmq_msg_init_data(zmq_msg,
                        ffi.cast('void*', message),
                        ffi.cast('size_t', 5),
                        ffi.NULL,
                        ffi.NULL)

    zmq_msg2 = ffi.new('zmq_msg_t')
    C.zmq_msg_init(zmq_msg2)

    ret = C.zmq_send(sender, zmq_msg, 0)
    ret2 = C.zmq_recv(receiver, zmq_msg2, 0)

    assert ret == ret2 == 0
    assert 5 == C.zmq_msg_size(zmq_msg2)
    assert "Hello" == str(ffi.cast('char*', C.zmq_msg_data(zmq_msg2)))

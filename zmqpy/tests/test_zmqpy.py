import unittest

class TestZmqpy(unittest.TestCase):
    def test_import_zmqpy(self):
        try:
            import zmqpy
            from zmqpy import Context, Socket
        except ImportError as ie:
            self.fail(ie.message)

class TestContext(unittest.TestCase):
    def tearDown(self):
        from zmqpy import Context
        c = Context()
        c.term()

    def test_context_init(self):
        from zmqpy import Context

        c = Context()
        cc = Context()

        assert type(c) == Context
        assert c.zmq_ctx
        assert c.n_sockets == 0
        assert c._sockets == {}
        assert c.closed == False
        assert c.iothreads == 1

        assert id(c.__dict__) == id(cc.__dict__)

    def test_context_term(self):
        from zmqpy import Context

        c = Context()

        c.term()

        assert c.closed
        assert c.zmq_ctx == None

    def test_context_socket(self):
        from zmqpy import Context, PAIR

        c = Context()
        socket = c.socket(PAIR)

        assert socket
        assert c.n_sockets == 1
        assert len(c._sockets) == 1
        assert not c.closed

    def test_context_socket_term(self):
        from zmqpy import Context, PAIR
        c = Context()
        socket = c.socket(PAIR)

        assert socket
        assert c.n_sockets == 1
        assert len(c._sockets) == 1
        assert not c.closed

        c.term()

        assert c.n_sockets == 0
        assert len(c._sockets) == 0
        assert socket.closed

class TestSocket(unittest.TestCase):
    def tearDown(self):
        from zmqpy import Context
        c = Context()
        c.term()

    def test_socket_bind(self):
        from zmqpy import Context, PAIR
        c = Context()
        socket = c.socket(PAIR)

        bind = socket.bind('tcp://*:3333')
        assert bind == 0

        socket.close()

    def test_socket_connect(self):
        from zmqpy import Context, PAIR
        c = Context()
        sender = c.socket(PAIR)
        receiver = c.socket(PAIR)

        bind = receiver.bind('tcp://*:3333')
        assert bind == 0

        connect = sender.connect('tcp://127.0.0.1:3333')
        assert connect == 0

        sender.close()
        receiver.close()

    def test_socket_disconnected_send(self):
        from zmqpy import Context, PAIR, NOBLOCK
        c = Context()
        socket = c.socket(PAIR)

        ret = socket.send("zmqpy test message", NOBLOCK)

        assert ret == -1
        assert socket.last_errno > 0

        socket.close()

    def test_socket_connected_send(self):
        from zmqpy import Context, PAIR
        c = Context()
        sender = c.socket(PAIR)
        receiver = c.socket(PAIR)

        bind = receiver.bind('tcp://*:3333')
        connect = sender.connect('tcp://127.0.0.1:333')

        ret = sender.send("zmqpy test message")

        assert ret == 0
        assert sender.last_errno == None

        sender.close()
        receiver.close()

    def test_socket_connected_recv(self):
        from zmqpy import Context, PAIR
        c = Context()
        sender = c.socket(PAIR)
        receiver = c.socket(PAIR)

        bind = receiver.bind('tcp://*:3333')
        connect = sender.connect('tcp://127.0.0.1:3333')

        assert bind == 0
        assert connect == 0

        ret = sender.send("zmqpy test message")

        assert ret == 0
        assert sender.last_errno == None

        import time
        time.sleep(0.2)
        message = receiver.recv()

        assert sender.last_errno == None
        assert message == "zmqpy test message"

        sender.close()
        receiver.close()

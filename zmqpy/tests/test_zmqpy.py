import unittest

class TestZmqpy(unittest.TestCase):
    def test_import_zmqpy(self):
        try:
            import zmqpy
            from zmqpy import Context, Socket, ZFrame
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

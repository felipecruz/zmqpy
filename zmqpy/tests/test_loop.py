# This test is part of the zmqpy implementation
import unittest

import zmqpy
from __init__ import BaseZMQTestCase

checklist = []

class TestLoop(BaseZMQTestCase):
    def test_loop(self):
        loop = zmqpy.Loop(verbose=True)
        s1, s2 = self.create_bound_pair(zmqpy.PAIR, zmqpy.PAIR)

        def timer_event(loop, item, args):
            zmqpy.czmq.zstr_send(args, 'message')
            return 0

        def socket_event(loop, item, args):
            return -1

        loop.timer(100, 1, timer_event, s1)

        from zmqpy import zmq_pollitem_t
        _input = zmq_pollitem_t(s2.handle, 0, zmqpy.POLLIN)

        loop.poller(_input, socket_event, s2.handle)

        loop.start()
        loop.destroy()

    def test_loop_poller_end(self):
        loop = zmqpy.Loop(verbose=True)
        s1, s2 = self.create_bound_pair(zmqpy.PAIR, zmqpy.PAIR)

        global checklist

        def socket_event(loop, item, args):
            checklist.append(1)
            if len(checklist) >= 2:
                return -1
            return 0

        from zmqpy import zmq_pollitem_t
        _input = zmq_pollitem_t(s2.handle, 0, zmqpy.POLLIN)

        import threading

        class LoopThread(threading.Thread):
            def __init__(self, loop):
                super(LoopThread, self).__init__()
                self.loop = loop

            def run(self):
                rc = self.loop.start()
                return rc

            def stop(self):
                self.loop.destroy()

        loop_thread = LoopThread(loop)

        loop.poller(_input, socket_event, None)
        s1.send('message 1')
        loop.poller_end(_input)
        s1.send('message 2')
        loop.poller(_input, socket_event, None)

        loop_thread.start()
        loop_thread.join()
        loop.destroy()
        self.assertTrue(len(checklist) == 2)

if __name__ == "__main__":
    unittest.main()


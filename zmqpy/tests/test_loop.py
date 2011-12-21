# This test is part of the zmqpy implementation
import unittest

import zmqpy
from __init__ import BaseZMQTestCase

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

        loop.poller(_input, socket_event, None)

        loop.start()
        loop.destroy()

   
if __name__ == "__main__":
    unittest.main()


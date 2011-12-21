# This test is part of the zmqpy implementation
#    
import unittest

import zmqpy
from __init__ import BaseZMQTestCase

class TestZFrames(BaseZMQTestCase):

    def test_new_zframe(self):
        frame = zmqpy.ZFrame()        
        frame_content = zmqpy.ZFrame("zmq message")

    def test_send_frame(self):
        s1, s2 = self.create_bound_pair(zmqpy.PAIR, zmqpy.PAIR)
        message = "zmq message"
        frame_content = zmqpy.ZFrame(message)
        rc = frame_content.send(s1, 2)
        self.assertTrue(rc == 0)

        frame_recv = zmqpy.ZFrame.recv(s2)
        self.assertEquals(message, "zmq message")

if __name__ == "__main__":
    unittest.main()


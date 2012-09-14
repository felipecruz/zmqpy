#
#    Copyright (c) 2010-2011 Brian E. Granger & Min Ragan-Kelley
#
#    This file is part of pyzmq.
#
#    pyzmq is free software; you can redistribute it and/or modify it under
#    the terms of the Lesser GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    pyzmq is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    Lesser GNU General Public License for more details.
#
#    You should have received a copy of the Lesser GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import time
import unittest

import zmqpy
from zmqpy.utils.strtypes import asbytes
from .__init__ import BaseZMQTestCase

#-----------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------

class TestPubSub(BaseZMQTestCase):
    # We are disabling this test while an issue is being resolved.
    def test_basic(self):
        s1, s2 = self.create_bound_pair(zmqpy.PUSH, zmqpy.PULL)
        msg1 = asbytes('message')
        s1.send(msg1)
        time.sleep(0.1)
        msg2 = s2.recv()  # This is blocking!
        self.assertEquals(msg1, msg2)

    def test_topic(self):
        s1, s2 = self.create_bound_pair(zmqpy.PUB, zmqpy.SUB)
        s2.setsockopt(zmqpy.SUBSCRIBE, asbytes('x'))
        time.sleep(0.1)
        msg1 = asbytes('message')
        s1.send(msg1)
        self.assertRaisesErrno(zmqpy.EAGAIN, s2.recv, zmqpy.NOBLOCK)
        msg1 = asbytes('xmessage')
        s1.send(msg1)
        msg2 = s2.recv()
        self.assertEquals(msg1, msg2)

if __name__ == "__main__":
    unittest.main()

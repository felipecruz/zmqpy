#
#    Copyright (c) 2010 Brian E. Granger
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

import unittest
import zmqpy
import time

from zmqpy.utils.strtypes import asbytes
from .__init__ import BaseZMQTestCase

#-----------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------


class TestContext(BaseZMQTestCase):

    def test_init(self):
        c1 = zmqpy.Context()
        self.assert_(isinstance(c1, zmqpy.Context))
        del c1
        c2 = zmqpy.Context()
        self.assert_(isinstance(c2, zmqpy.Context))
        del c2
        c3 = zmqpy.Context()
        self.assert_(isinstance(c3, zmqpy.Context))
        del c3

    def test_term(self):
        c = zmqpy.Context()
        c.term()
        self.assert_(c.closed)

    def test_fail_init(self):
        self.assertRaisesErrno(zmqpy.EINVAL, zmqpy.Context, 0)

    def test_instance_state(self):
        ctx = zmqpy.Context()
        c2 = zmqpy.Context(iothreads=2)
        self.assertTrue(ctx.iothreads)
        c2.term()
        self.assertTrue(ctx.closed)
        c3 = zmqpy.Context()
        c4 = zmqpy.Context()
        self.assertFalse(c3.closed)
        self.assertFalse(c4.closed)
        c4.term()
        self.assertTrue(ctx.closed)

    def test_term_hang(self):
        rep, req = self.create_bound_pair(zmqpy.XREP, zmqpy.XREQ)
        req.setsockopt(zmqpy.LINGER, 0)
        req.send(asbytes('hello'), copy=False)
        req.close()
        rep.close()
        self.context.term()

    def test_many_sockets(self):
        """opening and closing many sockets shouldn't cause problems"""
        ctx = self.context
        for i in range(16):
            sockets = [ ctx.socket(zmqpy.REP) for i in range(65) ]
            [ s.close() for s in sockets ]
            # give the reaper a chance
            time.sleep(1e-2)
        ctx.term()
        for s in sockets:
            self.assertTrue(s.closed)

    def test_term_close(self):
        """Context.term should close sockets"""
        sockets = [ self.context.socket(zmqpy.REP) for i in range(65) ]
        # close half of the sockets
        [ s.close() for s in sockets[::2] ]
        self.context.term()
        for s in sockets:
            self.assertTrue(s.closed)

    def test_set_linger(self):
        ctx = zmqpy.Context()
        self.assertEquals(ctx.linger, 1)

        ctx.set_linger(10)
        self.assertEquals(ctx.linger, 10)

if __name__ == "__main__":
    unittest.main()

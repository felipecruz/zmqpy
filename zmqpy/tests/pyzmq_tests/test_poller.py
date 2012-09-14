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

import time
import unittest

import zmqpy
from zmqpy.utils.strtypes import asbytes
from zmqpy import Poller
from .__init__ import BaseZMQTestCase

#-----------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------

class PollerTest(BaseZMQTestCase):
    def test_poller_init(self):
        poller = Poller()

        assert poller

    def test_poller_register(self):
        poller = Poller()
        socket1, socket2 = self.create_bound_pair(zmqpy.PAIR, zmqpy.PAIR)
        poller.register(socket1)

        assert poller.sockets[socket1] == zmqpy.POLLIN | zmqpy.POLLOUT

    def test_poller_register_no_flags(self):
        poller = Poller()
        socket1, socket2 = self.create_bound_pair(zmqpy.PAIR, zmqpy.PAIR)
        poller.register(socket1)

        #register with no flags unregister the socket
        poller.register(socket1, flags=None)

        assert poller.sockets == {}

    def test_poller_unregister(self):
        poller = Poller()
        socket1, socket2 = self.create_bound_pair(zmqpy.PAIR, zmqpy.PAIR)
        poller.register(socket1)

        #register with no flags unregister the socket
        poller.unregister(socket1)

        assert poller.sockets == {}

    def test_poller_modify(self):
        poller = Poller()
        socket1, socket2 = self.create_bound_pair(zmqpy.PAIR, zmqpy.PAIR)
        poller.register(socket1)

        #register with no flags unregister the socket
        poller.modify(socket1, flags=zmqpy.POLLOUT)

        assert poller.sockets[socket1] == zmqpy.POLLOUT

def wait():
    time.sleep(.25)

class TestPoll(BaseZMQTestCase):

    Poller = zmqpy.Poller

    # This test is failing due to this issue:
    # http://github.com/sustrik/zeromq2/issues#issue/26
    def test_pair(self):
        s1, s2 = self.create_bound_pair(zmqpy.PAIR, zmqpy.PAIR)

        # Sleep to allow sockets to connect.
        wait()

        poller = self.Poller()
        poller.register(s1, zmqpy.POLLIN|zmqpy.POLLOUT)
        poller.register(s2, zmqpy.POLLIN|zmqpy.POLLOUT)
        # Poll result should contain both sockets
        socks = dict(poller.poll())
        # Now make sure that both are send ready.
        self.assertEquals(socks[s1], zmqpy.POLLOUT)
        self.assertEquals(socks[s2], zmqpy.POLLOUT)
        # Now do a send on both, wait and test for zmqpy.POLLOUT|zmqpy.POLLIN
        s1.send(b'msg1')
        s2.send(b'msg2')
        wait()
        socks = dict(poller.poll())
        self.assertEquals(socks[s1], zmqpy.POLLOUT|zmqpy.POLLIN)
        self.assertEquals(socks[s2], zmqpy.POLLOUT|zmqpy.POLLIN)
        # Make sure that both are in POLLOUT after recv.
        s1.recv()
        s2.recv()
        socks = dict(poller.poll())
        self.assertEquals(socks[s1], zmqpy.POLLOUT)
        self.assertEquals(socks[s2], zmqpy.POLLOUT)

        poller.unregister(s1)
        poller.unregister(s2)

        # Wait for everything to finish.
        wait()

    def test_reqrep(self):
        s1, s2 = self.create_bound_pair(zmqpy.REP, zmqpy.REQ)

        # Sleep to allow sockets to connect.
        wait()

        poller = self.Poller()
        poller.register(s1, zmqpy.POLLIN|zmqpy.POLLOUT)
        poller.register(s2, zmqpy.POLLIN|zmqpy.POLLOUT)

        # Make sure that s1 is in state 0 and s2 is in POLLOUT
        socks = dict(poller.poll())
        self.assertEquals(s1 in socks, 0)
        self.assertEquals(socks[s2], zmqpy.POLLOUT)

        # Make sure that s2 goes immediately into state 0 after send.
        s2.send(b'msg1')
        socks = dict(poller.poll())
        self.assertEquals(s2 in socks, 0)

        # Make sure that s1 goes into POLLIN state after a time.sleep().
        time.sleep(0.5)
        socks = dict(poller.poll())
        self.assertEquals(socks[s1], zmqpy.POLLIN)

        # Make sure that s1 goes into POLLOUT after recv.
        s1.recv()
        socks = dict(poller.poll())
        self.assertEquals(socks[s1], zmqpy.POLLOUT)

        # Make sure s1 goes into state 0 after send.
        s1.send(b'msg2')
        socks = dict(poller.poll())
        self.assertEquals(s1 in socks, 0)

        # Wait and then see that s2 is in POLLIN.
        time.sleep(0.5)
        socks = dict(poller.poll())
        self.assertEquals(socks[s2], zmqpy.POLLIN)

        # Make sure that s2 is in POLLOUT after recv.
        s2.recv()
        socks = dict(poller.poll())
        self.assertEquals(socks[s2], zmqpy.POLLOUT)

        poller.unregister(s1)
        poller.unregister(s2)

        # Wait for everything to finish.
        wait()

    def test_no_events(self):
        s1, s2 = self.create_bound_pair(zmqpy.PAIR, zmqpy.PAIR)
        poller = self.Poller()
        poller.register(s1, zmqpy.POLLIN|zmqpy.POLLOUT)
        poller.register(s2, 0)
        self.assertTrue(s1 in poller.sockets)
        self.assertFalse(s2 in poller.sockets)
        poller.register(s1, 0)
        self.assertFalse(s1 in poller.sockets)

    def test_pubsub(self):
        s1, s2 = self.create_bound_pair(zmqpy.PUB, zmqpy.SUB)
        s2.setsockopt(zmqpy.SUBSCRIBE, b'')

        # Sleep to allow sockets to connect.
        wait()

        poller = self.Poller()
        poller.register(s1, zmqpy.POLLIN|zmqpy.POLLOUT)
        poller.register(s2, zmqpy.POLLIN)

        # Now make sure that both are send ready.
        socks = dict(poller.poll())
        self.assertEquals(socks[s1], zmqpy.POLLOUT)
        self.assertEquals(s2 in socks, 0)
        # Make sure that s1 stays in POLLOUT after a send.
        s1.send(b'msg1')
        socks = dict(poller.poll())
        self.assertEquals(socks[s1], zmqpy.POLLOUT)

        # Make sure that s2 is POLLIN after waiting.
        wait()
        socks = dict(poller.poll())
        self.assertEquals(socks[s2], zmqpy.POLLIN)

        # Make sure that s2 goes into 0 after recv.
        s2.recv()
        socks = dict(poller.poll())
        self.assertEquals(s2 in socks, 0)

        poller.unregister(s1)
        poller.unregister(s2)

        # Wait for everything to finish.
        wait()
    def test_timeout(self):
        """make sure Poller.poll timeout has the right units (milliseconds)."""
        s1, s2 = self.create_bound_pair(zmqpy.PAIR, zmqpy.PAIR)
        poller = self.Poller()
        poller.register(s1, zmqpy.POLLIN)
        tic = time.time()
        evt = poller.poll(timeout=.005)
        toc = time.time()
        self.assertTrue(toc-tic < 0.1)
        tic = time.time()
        evt = poller.poll(timeout=5)
        toc = time.time()
        self.assertTrue(toc-tic < 0.1)
        self.assertTrue(toc-tic > .001)
        tic = time.time()
        evt = poller.poll(timeout=500)
        toc = time.time()
        self.assertTrue(toc-tic < 1)
        self.assertTrue(toc-tic > 0.1)

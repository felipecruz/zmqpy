zmqpy - (cffi) zeromq python bindings
=====================================

**This code is a work in progress**

The goal of this project is to provide a CPython/PyPy compatible ZeroMQ bindings
for the Python language.

It uses cffi (http://cffi.readthedocs.org) as integration mechanism with the 
original code.

API Example
-----------

It looks like Pyzmq.

```python

import zmqpy

context = zmqpy.Context()

socket = context.socket(zmqpy.PUSH)
socket.bind('tcp://127.0.0.1:5555')

socket.send('message', zmqpy.NOBLOCK)

socket.close()
context.term()

```

Tests
-----

First time:

`pip install -r requirements.txt`

To actually run the tests:

`make test`

Coverage Report
---------------

First time:

`pip install -r coverage_requirements.txt`

And then:

`make coverage`

zmqpy - alternate (cffi) zeromq python bindings
=====================================

[![Build Status](https://secure.travis-ci.org/felipecruz/zmqpy.png?branch=master)](https://travis-ci.org/felipecruz/zmqpy)


zmqpy is already compatible with zeromq 2.2.x and 3.2.1.

The goal of this project is to provide a CPython/PyPy compatible ZeroMQ bindings
for the Python language.

It uses cffi (http://cffi.readthedocs.org) as integration mechanism with the
original libzmq code.

Install
-------

From PyPi

```sh
pip install zmqpy
```

Install from source

```sh
git clone https://github.com/felipecruz/zmqpy.git
python setup.py install
```

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

Troubleshooting - Custom prefix zeromq installation
---------------------------------------------------

If you installed zeromq with a custom prefix you may run into some errors.

If you find any errors regarding not found `libzmq.so` or `zmq.h` you may have to export 2 environment variables: `C_INCLUDE_PATH` and `LD_LIBRARY_PATH`. It's very important
to `export` them so they'll be also available for subprocesses. Usually you export `C_INCLUDE_PATH` to your custom installation header directory and `LD_LIBRARY_PATH` 
to the `libzmq.so` installed directory.

Benchmarks
----------

This (naive) benchmark compares PyPy + zmqpy Vs Cpython + PyZMQ

It sends *10000000* 10 bytes message == "aaaaaaaaaa".

PyPy(*Trunk*) with Cffi

```sh
(pypy19)felipecruz:benchmarks/ (master*) $ time python sender.py
python sender.py  12.29s user 7.17s system 182% cpu 10.672 total
(pypy19)felipecruz:benchmarks/ (master*) $ time python sender.py
python sender.py  12.63s user 7.38s system 182% cpu 10.945 total
(pypy19)felipecruz:benchmarks/ (master*) $ time python sender.py
python sender.py  12.29s user 7.18s system 183% cpu 10.617 total
```

Python 2.7 + PyZMQ

```sh
(py27)felipecruz:benchmarks/ (master*) $ time python sender.py
python sender.py  25.86s user 18.67s system 191% cpu 23.279 total
(py27)felipecruz:benchmarks/ (master*) $ time python sender.py
python sender.py  25.93s user 18.57s system 190% cpu 23.386 total
(py27)felipecruz:benchmarks/ (master*) $ time python sender.py
python sender.py  26.79s user 19.24s system 190% cpu 24.109 total
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

`pip install -r requirements.txt`

And then:

`make coverage`

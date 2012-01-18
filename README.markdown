zmqpy - czmq/ctypes zeromq library in python
============================================

**This code is a work in progress**

The goal is to provide a zmq library compatible with the python/pypy implementation and to provide an event-driver reactor instead of a poll-like interface.

Install czmq library from my repository: https://github.com/felipecruz/czmq

You'll need py.test - http://pytest.org/latest/

<pre>
python runtests.py
</pre>

Test environments

* osx 64 - pypy 1.7 - zmq 2.x, 3.x
* linux 32 - pypy 1.7 - zmq 2.x
* linux 32 - python 2.7.2 - zmq 2.x
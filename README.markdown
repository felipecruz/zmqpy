zmqpy - zeromq bindings in python
============================================

**This code is a work in progress**

The goal is to provide a zmq library compatible with the python/pypy implementation and to provide an event-driver reactor instead of a poll-like interface.

It is kind of pointless use zmqpy with ctypes, since ctypes current implementation is **really** slow and segfaults on OSX.

There is this new, and very promissing project, called cffi (http://cffi.readthedocs.org/) that allows zmqpy to be
a reasonable alternative to pyzmq since it not segfaults (so far) and is much faster than the ctypes one.

This project still exprimental but with cffi It'll be possible to create a production ready zmq biding for python.

Install czmq library : https://github.com/zeromq/czmq

You'll need py.test - http://pytest.org/latest/

<pre>
python runtests.py
</pre>

Test environments:

<table>
  <th>
    <td>linux</td>
    <td>osx</td>
  </th>
  <tr>
    <td>python 2.7.2 zmq 2.x</td>
    <td>ok</td>
    <td>--</td>
  </tr>
  <tr>
    <td>python 2.7.2 zmq 3.x</td>
    <td>ok</td>
    <td>--</td>
  </tr>
  <tr>
    <td>pypy 1.7 zmq 2.x</td>
    <td>ok</td>
    <td>ok</td>
  </tr>
  <tr>
    <td>pypy 1.7 zmq 3.x</td>
    <td>ok</td>
    <td>ok</td>
  </tr>
</table>

*python 2.6.x and 2.7.2 both fail with segmentation fault on macosx 64 10.6.8*

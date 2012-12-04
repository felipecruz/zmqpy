'''
Created on May 20, 2010

@author: felipe
'''

from distutils.core import setup

setup(name='zmqpy',
      version='0.1a',
      description='Python czmq ctypes bindings',
      author='Felipe Cruz',
      author_email='fealipecruz@loogica.net',
      url='http://test.com',
     packages=['zmqpy', 'zmqpy/tests/', 'zmqpy/utils/'],
      requires=['cffi (==0.3)'],
     )

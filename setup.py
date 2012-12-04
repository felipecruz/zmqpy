from distutils.core import setup
import zmqpy._cffi

setup(name='zmqpy',
      version='0.2',
      description='Python cffi-based ZeroMQ bindings',
      author='Felipe Cruz',
      author_email='felipecruz@loogica.net',
      url='http://loogica.net/opensource/',
      install_requires=['cffi >=0.3'],
      packages=['zmqpy', 'zmqpy/tests/', 'zmqpy/utils/'])

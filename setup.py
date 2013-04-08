from setuptools import setup

setup(name='zmqpy',
      version='0.3.2',
      description='Python cffi-based ZeroMQ bindings',
      author='Felipe Cruz',
      author_email='felipecruz@loogica.net',
      url='http://loogica.net/opensource/',
      install_requires=['cffi>=0.3'],
      packages=['zmqpy', 'zmqpy/tests/', 'zmqpy/utils/',
                'zmqpy/tests/pyzmq_tests/'])

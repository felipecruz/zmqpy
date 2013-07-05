from setuptools import setup

setup(name='zmqpy',
      version='0.3.3',
      description='Python cffi-based ZeroMQ bindings',
      author='Felipe Cruz',
      author_email='felipecruz@loogica.net',
      url='https://github.com/felipecruz/zmqpy',
      install_requires=['cffi>=0.3'],
      packages=['zmqpy', 'zmqpy/tests/', 'zmqpy/utils/', 'zmqpy/eventloop',
                'zmqpy/tests/pyzmq_tests/'])

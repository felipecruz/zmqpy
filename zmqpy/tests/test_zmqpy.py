import unittest

class TestZmqpy(unittest.TestCase):
    def test_import_zmqpy(self):
        try:
            import zmqpy
            from zmqpy import zmqpy
        except ImportError as ie:
            self.fail(ie.message)



if __name__ == "__main__":
    unittest.main()

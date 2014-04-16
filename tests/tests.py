from protowrapper import Protowrapper, ValidationError
from test_pb2 import Address
import unittest

class TestSerializable(unittest.TestCase):

    def test_validation(self):

        class Address(Protowrapper):
            def check_ip(self):
                return len(self.ip) == 4
            def check_port(self):
                return self.port >= 0 and self.port <= 1000

        self.assertRaises(ValidationError, Address, ip=b'', port=500)
        self.assertRaises(ValidationError, Address, ip=b'1234', port=1001)
        test = Address(ip=b'1234',port=1000)

    def test_init(self):

        counter = 0

        class Address(Protowrapper):
            def init(self):
                nonlocal counter
                counter += 1

        Address(ip=b'1234',port=1000)
        Address(ip=b'1234',port=1000)
        Address(ip=b'1234',port=1000)
        self.assertEqual(counter,3)



if __name__ == '__main__':
    unittest.main()

import unittest
from lab0 import *

class TestTask1(unittest.TestCase):
    # test encode hex
    def test_encode_1(self):
        self.assertEqual(bytes_to_hex(b'hello'), '68656c6c6f')

    def test_encode_2(self):
        self.assertEqual(bytes_to_hex(b'world'), '776f726c64')

    def test_encode_3(self):
        self.assertEqual(bytes_to_hex(b''), '')

    # test decode hex
    def test_decode_1(self):
        self.assertEqual(hex_to_bytes('68656c6c6f'), b'hello')

    def test_decode_2(self):
        self.assertEqual(hex_to_bytes('776f726c64'), b'world')

    def test_decode_3(self):    
        self.assertEqual(hex_to_bytes(''), b'')

    # test encode base64
    def test_encode_4(self):
        self.assertEqual(bytes_to_base64(b'hello'), 'aGVsbG8=')

    def test_encode_5(self):
        self.assertEqual(bytes_to_base64(b'world'), 'd29ybGQ=')

    def test_encode_6(self):
        self.assertEqual(bytes_to_base64(b''), '')

    # test decode base64
    def test_decode_4(self):
        self.assertEqual(base64_to_bytes('aGVsbG8='), b'hello')

    def test_decode_5(self):    
        self.assertEqual(base64_to_bytes('d29ybGQ='), b'world')

    def test_decode_6(self):
        self.assertEqual(base64_to_bytes(''), b'')

class TestTask2(unittest.TestCase):
    # test xor
    def test_xor_1(self):
        self.assertEqual(xor(b'hello', b'world'), b'\x1f\n\x1e\x00\x0b')

    def test_xor_2(self):
        self.assertEqual(xor(b'world', b'hello'), b'\x1f\n\x1e\x00\x0b')

    def test_xor_3(self):
        self.assertEqual(xor(b'', b'hello'), b'')

    def test_xor_4(self):
        self.assertEqual(xor(b'', b''), b'')

    def test_xor_5(self):
        self.assertEqual(xor(b'hello', b'wow'), b'\x1f\n\x1b\x1b\x00')

if __name__ == '__main__':
    unittest.main()
import unittest
from padding import pad, unpad

class PaddingTest(unittest.TestCase):
    def test_pad(self):
        self.assertEqual(pad(b"YELLOW SUBMARINE", 20), b"YELLOW SUBMARINE\x04\x04\x04\x04")
        self.assertEqual(pad(b"YELLOW SUBMARINE", 16), b"YELLOW SUBMARINE\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10")
        self.assertEqual(pad(b"YELLOW SUBMARINE", 10), b"YELLOW SUBMARINE\x04\x04\x04\x04")
        self.assertEqual(pad(b"YELLOW SUBMARINE", 8), b"YELLOW SUBMARINE\x08\x08\x08\x08\x08\x08\x08\x08")
        self.assertEqual(pad(b"YELLOW SUBMARINE", 4), b"YELLOW SUBMARINE\x04\x04\x04\x04")


    def test_unpad(self):
        self.assertEqual(unpad(b"YELLOW SUBMARINE\x04\x04\x04\x04"), b"YELLOW SUBMARINE")
        self.assertEqual(unpad(b"YELLOW SUBMARINE\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10"), b"YELLOW SUBMARINE")
        self.assertEqual(unpad(b"YELLOW SUBMARINE\x04\x04\x04\x04"), b"YELLOW SUBMARINE")
        self.assertEqual(unpad(b"YELLOW SUBMARINE\x08\x08\x08\x08\x08\x08\x08\x08"), b"YELLOW SUBMARINE")
        self.assertEqual(unpad(b"YELLOW SUBMARINE\x04\x04\x04\x04"), b"YELLOW SUBMARINE")


    def test_pad_empty(self):
        self.assertEqual(pad(b"", 4), b"\x04\x04\x04\x04")
        self.assertEqual(pad(b"", 8), b"\x08\x08\x08\x08\x08\x08\x08\x08")


    def test_pad_invalid_block_size(self):
        with self.assertRaises(ValueError):
            pad(b"YELLOW SUBMARINE", 0)
        with self.assertRaises(ValueError):
            pad(b"YELLOW SUBMARINE", 256)
        with self.assertRaises(ValueError):
            pad(b"YELLOW SUBMARINE", -1)


    def test_unpad_invalid_padding(self):
        with self.assertRaises(ValueError):
            unpad(b"YELLOW SUBMARINE\x04\x04\x04\x05")
        with self.assertRaises(ValueError):
            unpad(b"YELLOW SUBMARINE\x03\x04\x04\x04")
        with self.assertRaises(ValueError):
            unpad(b"YELLOW SUBMARINE\x04\x04\x00\x04")


    def test_unpad_invalid_padding_length(self):
        with self.assertRaises(ValueError):
            unpad(b"YELLOW SUBMARINE\x00\x00\x00\x00")
        with self.assertRaises(ValueError):
            unpad(b"YELLOW SUBMARINE\x03\x03")


if __name__ == "__main__":
    unittest.main()
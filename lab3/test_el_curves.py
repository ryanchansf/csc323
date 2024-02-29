from el_curves import *
import unittest

class TestElCurves(unittest.TestCase):
    def setUp(self):
        self.curve = EllipticCurve(3, 8, 13)
    
    # point addition tests
    def test_add(self):
        p = Point(9, 7)
        q = Point(1, 8)
        actual = point_addition(p, q, self.curve)
        expected = Point(2, 10)
        self.assertEqual(actual, expected)
        
    def test_add_2(self):
        p = Point(9, 7)
        q = Point(9, 7)
        actual = point_addition(p, q, self.curve)
        expected = Point(9, 6)
        self.assertEqual(actual, expected)
        
    def test_add_3(self):
        p = Point(12, 11)
        q = Point(12, 2)
        actual = point_addition(p, q, self.curve)
        expected = Point(0, 0)
        self.assertEqual(actual, expected)
        
    # point multiplication tests
    def test_mult(self):
        p = Point(9, 7)
        n = 1
        actual = point_multiplication(p, n, self.curve)
        expected = Point(9, 7)
        self.assertEqual(actual, expected)
        
    def test_mult_2(self):
        p = Point(9, 7)
        n = 2
        actual = point_multiplication(p, n, self.curve)
        expected = Point(9, 6)
        self.assertEqual(actual, expected)
        
    def test_mult_3(self):
        p = Point(9, 7)
        n = 3
        actual = point_multiplication(p, n, self.curve)
        expected = Point(0, 0)
        self.assertEqual(actual, expected)
        
    def test_mult_4(self):
        p = Point(9, 7)
        n = 4
        actual = point_multiplication(p, n, self.curve)
        expected = Point(9, 7)
        self.assertEqual(actual, expected)
        
        
if __name__ == "__main__":
    unittest.main()
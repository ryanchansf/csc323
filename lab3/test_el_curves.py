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
        
    def test_tonnelli_shanks(self):
        n = 3
        p = 13
        actual = tonnelli_shanks(n, p)
        expected = 9
        self.assertEqual(actual, expected)
        
    def test_tonnelli_shanks_1(self):
        n = 5
        p = 13
        actual = tonnelli_shanks(n, p)
        expected = -1
        self.assertEqual(actual, expected)
        
    def test_tonnelli_shanks_2(self):
        n = 44
        p = 83
        actual = tonnelli_shanks(n, p)
        expected = 25
        self.assertEqual(actual, expected)
        
    def test_random_point(self):
        p = random_point(self.curve)
        left = pow(p.y, 2, self.curve.f)
        right = pow(pow(p.x, 3) + self.curve.a * p.x + self.curve.b, 1, self.curve.f)
        self.assertEqual(left, right)
        
        
if __name__ == "__main__":
    unittest.main()
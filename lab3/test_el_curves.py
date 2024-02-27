from el_curves import *
import unittest

class TestElCurves(unittest.TestCase):
    def test_add(self):
        p = Point(9, 7)
        q = Point(1, 8)
        ec = EllipticCurve(3, 8, 13)
        expected = Point(2, 10)
        self.assertEqual(point_addition(p, q, ec).x, expected.x)
        self.assertEqual(point_addition(p, q, ec).y, expected.y)
        
        
if __name__ == "__main__":
    unittest.main()
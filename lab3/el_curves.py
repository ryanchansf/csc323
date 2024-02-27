class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
  
        
class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p


def point_doubling(p: Point, ec: EllipticCurve) -> Point:
    """
    Takes in a point and an elliptic curve and returns the doubling of the point.
    """
    m = (3 * p.x**2 + ec.a) / (2 * p.y)
    x = (m**2 - 2 * p.x) % ec.p
    y = (m * (p.x - x) - p.y) % ec.p
    return Point(x, y)


def point_addition(p: Point, q: Point, ec: EllipticCurve) -> Point:
    """
    Takes in two points and an elliptic curve and returns the sum of the two points.
    """
    # point at infinity
    if p.x == q.x and p.y == q.y:
        return point_doubling(p, ec)
    # vertical line
    if p.x == q.x and p.y != q.y:
        return Point(float("inf"), float("inf"))
    m = (q.y - p.y) / (q.x - p.x)
    x = (m**2 - p.x - q.x) % ec.p
    y = (m * (x - p.x) + p.y) % ec.p
    return Point(x, y)


def point_multiplication(p: Point, n: int, ec: EllipticCurve) -> Point:
    """
    Takes in a point and a scalar and utilizes the double-add algorithm to return the product of the point and the scalar.
    Pseudocode:
    1. R ← O
    2. repeat
    3.  if n mod 2 == 1 then
    4.     R ← R + p
    5.  end if
    6.  p ← 2g
    7.  n ← n div 2
    8. until n = 0
    """
    r = Point(float("inf"), float("inf"))
    while n > 0:
        if n % 2 == 1:
            r = point_addition(r, p, ec)
        p = point_doubling(p, ec)
        n = n // 2
    return r


if __name__ == "__main__":
    ec = EllipticCurve(3, 8, 13)
    p = Point(9, 7)
    q = Point(1, 8)
    print(point_addition(p, q, ec).x, point_addition(p, q, ec).y)
    # n = 5
    # print(point_multiplication(p, n, ec).x, point_multiplication(p, n, ec).y)
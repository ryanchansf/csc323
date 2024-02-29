class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"
  
        
class EllipticCurve:
    def __init__(self, a, b, f):
        self.a = a
        self.b = b
        self.f = f


def point_addition(p: Point, q: Point, ec: EllipticCurve) -> Point:
    """
    Takes in two points and an elliptic curve and returns the sum of the two points.
    """
    # point at infinity
    if q == Point(0, 0):
        return p
    elif p == Point(0, 0):
        return q
    # vertical line
    elif p.x == q.x and p.y != q.y:
        return Point(0, 0)
    # different points
    elif p != q:
        # find slope of the line between points
        m = (q.y - p.y) * pow(q.x - p.x, -1, ec.f)
    else:
        # find slope of the tangent line
        m = (3 * pow(p.x, 2, ec.f) + ec.a) * pow(2 * p.y, -1, ec.f)
    m = pow(m, 1, ec.f)
    x = pow((pow(m, 2, ec.f) - p.x - q.x), 1, ec.f)
    y = pow((m * (p.x - x) - p.y), 1, ec.f)
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
    r = Point(0, 0)
    while n > 0:
        if pow(n, 1, 2) == 1:
            # add p to r
            r = point_addition(r, p, ec)
        # double p
        p = point_addition(p, p, ec)
        n = n // 2
    return r


if __name__ == "__main__":
    ec = EllipticCurve(3, 8, 13)
    p = Point(9, 7)
    q = Point(1, 8)
    print(point_addition(p, q, ec))
    
    n = 5
    print(point_multiplication(p, 5, ec))
    
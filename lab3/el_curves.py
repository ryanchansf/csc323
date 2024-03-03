import random

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


def tonnelli_shanks(n: int, p: int) -> int:
    """
    Returns the square root of n (mod p) in the field p using the Tonelli-Shanks algorithm.
    """
    # find q and s
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    # find a quadratic non-residue
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1
    # initialize variables
    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) // 2, p)
    # loop
    while t != 1:
        if t == 0:
            return 0
        # find the smallest i such that t^(2^i) = 1 (mod p)
        i = 0
        temp = t
        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1
        # no solution to congruence exists
        if i == m:
            # n is not a quadratic residue
            return -1
        # update variables
        b = pow(c, pow(2, m - i - 1, p), p)
        m = i
        c = pow(b, 2, p)
        t = pow((t * c), 1, p)
        r = pow((r * b), 1, p)
    return r


def random_point(ec: EllipticCurve) -> Point:
    """
    Returns a random point on the elliptic curve using the Tonelli-Shanks algorithm.
    Steps:
    1. Pick a random x in the field.
    2. Calculate y^2 = x^3 + ax + b mod f.
    3. Since n = y^2 (mod f), find the square root of n in f
        a. Note that not all such n have a square root in f. 
        The ones that do are called quadratic residues, and 
        you can check if your n is a quadratic residue using 
        Euler's Criterion. If it isn't, just pick another 
        random x and try again.
        b. This can be done using the Tonelli-Shanks algorithm.
    """
    # pick a random x in the field
    x = random.randint(0, ec.f - 1)
    y_squared = pow((pow(x, 3, ec.f) + ec.a * x + ec.b), 1, ec.f)
    n = pow(y_squared, 1, ec.f)
    # use Tonelli-Shanks algorithm to find the square root of n in f
    # check if n is a quadratic residue
    y = tonnelli_shanks(n, ec.f)
    if y == -1:
        return random_point(ec)
    return Point(x, y)


if __name__ == "__main__":
    ec = EllipticCurve(3, 8, 13)
    p = Point(9, 7)
    q = Point(1, 8)
    print(point_addition(p, q, ec))
    
    n = 5
    print(point_multiplication(p, 5, ec))
    
    print(tonnelli_shanks(5, 13)) # no quadratic residue
    print(tonnelli_shanks(44, 83)) # quadratic residue
    
    print(random_point(ec))
    
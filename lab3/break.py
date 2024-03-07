from el_curves import *
import requests
from bs4 import BeautifulSoup
from Crypto.Hash import HMAC, SHA256

def calculate_hmac(message: str, shared_key: Point) -> str:
    hmac = HMAC.new(str(shared_key).encode(), digestmod=SHA256)
    hmac.update(message.encode())
    return hmac.hexdigest()


def request_server(message: str, hmac: str, p_key: Point, recipient: str) -> str:
    url = "http://localhost:8080/submit"
    data = {
        "recipient": recipient,
        "message": message,
        "hmac": hmac,
        "pkey_x": str(p_key.x),
        "pkey_y": str(p_key.y),
    }
    response = requests.post(url, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    texts = soup.find_all("font", color="black")
    admin_message = texts[0].text.strip()
    server_hmac = texts[1].text.split(": ")[1].strip()
    return admin_message, server_hmac


def secret_key_mod_8(server_hmac: str, message: str, p_key: Point, curve: EllipticCurve) -> int:
    """
    Given the public key and message, use brute force to find the secret key mod 8.
    """
    try:
        for i in range(8):
            # generate different shared keys by multiplying the p_key by different scalers in range 8
            sh_key = point_multiplication(p_key, i, curve)
            hmac = calculate_hmac(message, sh_key)
            print("HMAC:", hmac)
            if hmac == server_hmac:
                return i
        return -1
    except ValueError:
        raise ValueError("Secret key mod 8 error")


def find_admin_key(curve: EllipticCurve) -> str:
    # initialize curve and keys
    x = 16349894185180983439102154383611486412
    y = 224942997200586455214256137069604954919
    p_key = Point(x, y)
    order = 8
    sh_key = "dummy key"
    
    # initialize message data
    recipient = "Admin"
    message = "Hello, Admin!"
    hmac = calculate_hmac(message, sh_key)
    
    # server hmac corresponds to the message and shared key
    admin_message, server_hmac = request_server(message, hmac, p_key, recipient)
    print("admin_message:", admin_message)
    print("server_hmac:", server_hmac)
    
    # given the message and generated hmac, find the admin's secret key
    # since the order is 8, we can use the brute force method
    partial_secret_key = secret_key_mod_8(server_hmac, admin_message, p_key, curve)
    return partial_secret_key
    

def get_admin_secret_key(curves: list[EllipticCurve], order: int) -> int:
    factor_bank = set()
    admin_key_mod_factors = []
    # get the admin's secret key mod all prime factors of curves
    for curve in curves:
        keys = get_remainders(curve, factor_bank)
        for factor, admin_key_mod_factor in keys:
            admin_key_mod_factors.append(
                (factor, admin_key_mod_factor))
            factor_bank.add(factor)

    # verify the product of all the factors is greater than the order
    product = 1
    for factor, _ in admin_key_mod_factors:
        product *= factor
    if product < order:
        raise ValueError("Product of factors is less than the order")
    
    # find the admin's secret key using the Chinese Remainder Theorem
    admin_secret_key = 0
    for factor, admin_key_remainder in admin_key_mod_factors:
        m = product // factor
        m_inv = pow(m, -1, factor)
        admin_secret_key += admin_key_remainder * m * m_inv
    admin_secret_key %= product
    print("Admin secret key:", admin_secret_key)
    return admin_secret_key



def get_remainders(curve: EllipticCurve, factor_bank: set[int]) -> list[tuple[int, int]]:
    """
    Get a list of admin keys mod the prime factors of the curve's order
    """
    prime_factors = prime_factors_up_to_n(curve.o, pow(2, 16))

    admin_key_mod_factors = []
    for factor in prime_factors:
        if factor not in factor_bank:
            # haven't found admin key mod this factor
            message = "aaaaaaaa"
            shared_key = "bbbbbbb"
            hmac = calculate_hmac(message, shared_key)
            # get a random point with order of factor
            public_key = random_point_order(curve, factor)
            if public_key is None:
                print("pass no public key")
                continue
            # get admin response
            admin_message, admin_hmac = request_server(message, hmac, public_key, "Admin")

            # task III - find the admin key mod the factor
            admin_key_mod_factor = get_admin_key_mod_factor(curve, admin_message, admin_hmac, public_key, factor)
            if admin_key_mod_factor != -1:
                admin_key_mod_factors.append((factor, admin_key_mod_factor))
            else:
                print("pass no key")
    return admin_key_mod_factors


def get_admin_key_mod_factor(curve: EllipticCurve, admin_msg: str, admin_hmac: str, pkey: Point, factor: int) -> int:
    for i in range(factor):
        shared_key = point_multiplication(pkey, i, curve)
        test_hmac = calculate_hmac(
            admin_msg, shared_key)
        if admin_hmac == test_hmac:
            return i
    return -1


def prime_factors_up_to_n(x: int, n: int) -> list[int]:
    """
    Generate the prime factors of x up to n using the Sieve of Eratosthenes
    """
    D = {}
    q = 2
    result = []
    while q < n:
        if q not in D:
            if x % q == 0:
                result.append(q)
            D[q * q] = [q]
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        q += 1
    return result
    
if __name__ == "__main__":
    main_curve = EllipticCurve(-95051, 11279326, 233970423115425145524320034830162017933, 29246302889428143187362802287225875743)
    base_point = Point(182, 85518893674295321206118380980485522083)
    ref_curves = [
        EllipticCurve(-95051, 118, 233970423115425145524320034830162017933,
                      233970423115425145528637034783781621127),
        EllipticCurve(-95051, 727, 233970423115425145524320034830162017933,
                      233970423115425145545378039958152057148),
        EllipticCurve(-95051, 210, 233970423115425145524320034830162017933,
                      233970423115425145550826547352470124412),
        EllipticCurve(834, 11279326, 233970423115425145524320034830162017933,
                      233970423115425145548264999925929157572),
        EllipticCurve(102, 11279326, 233970423115425145524320034830162017933,
                      233970423115425145509961303666413107064),
        EllipticCurve(-95051, 79, 233970423115425145524320034830162017933,
                      233970423115425145538546862144009931013),
        EllipticCurve(31, 11279326, 233970423115425145524320034830162017933,
                      233970423115425145499771890762612355342),
        EllipticCurve(-95051, 504, 233970423115425145524320034830162017933,
                      233970423115425145544350131142039591210),
        EllipticCurve(303, 11279326, 233970423115425145524320034830162017933,
                      233970423115425145535467383967616574919),
        EllipticCurve(516, 11279326, 233970423115425145524320034830162017933,
                      233970423115425145519589093288869640865)
    ]
    admin_secret_key = get_admin_secret_key(ref_curves, main_curve.o)
    # send message to bob
    msg = "Hello as admin!"
    recipient = "Bob"
    public_key = point_multiplication(base_point, admin_secret_key, main_curve)
    # get bob's public key from server
    req = requests.get("http://localhost:8080/users")
    soup = BeautifulSoup(req.text, "html.parser")
    elements = soup.find_all("td")
    x, y = elements[3].text.strip()[1:-1].split(", ")
    bob_public_key = Point(int(x), int(y))
    # calculate shared key and hmac
    shared_key = point_multiplication(bob_public_key, admin_secret_key, main_curve)
    hmac = calculate_hmac(msg, shared_key)
    # send message to bob
    print(request_server(msg, hmac, public_key, recipient))
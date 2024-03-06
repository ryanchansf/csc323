from el_curves import *
import requests
from bs4 import BeautifulSoup
from Crypto.Hash import HMAC, SHA256

def calculate_hmac(message: str, key: Point) -> str:
    hmac = HMAC.new(str(key).encode(), digestmod=SHA256)
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
    admin_message = texts[0].text
    server_hmac = texts[1].text.split(": ")[1]
    return admin_message, server_hmac


def find_admin_key(curve: EllipticCurve, base_point_order: int) -> int:
    # initialize curve and keys
    x = 16349894185180983439102154383611486412
    y = 224942997200586455214256137069604954919
    p_key = Point(x, y)
    order = 8
    sh_key = "shared_key"
    
    # initialize message data
    recipient = "Admin"
    message = "Hello Admin"
    hmac = calculate_hmac(message, sh_key)
    print("HMAC:", hmac)
    
    admin_message, server_hmac = request_server(message, hmac, p_key, recipient)
    print("admin_message:", admin_message)
    print("server_hmac:", server_hmac)
    
    # given the message and generated hmac, find the admin's secret key
    # since the order is 8, we can use the brute force method
    # generate different shared keys by multiplying the p_key by different scalers in range 8
    return -1
    
    
if __name__ == "__main__":
    curve = EllipticCurve(-95051, 11279326, 233970423115425145524320034830162017933)
    base_point_order = 29246302889428143187362802287225875743
    find_admin_key(curve, base_point_order)
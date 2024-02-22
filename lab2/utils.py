import base64

def bytes_to_hex(byte_string):
    """
    Encodes a string of bytes to a hex-encoded ASCII string
    """
    return byte_string.hex()


def hex_to_bytes(hex_string):
    """
    Decodes a hex-encoded ASCII string to a string of bytes
    """
    return bytes.fromhex(hex_string)

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
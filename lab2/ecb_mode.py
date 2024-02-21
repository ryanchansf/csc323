from Crypto.Cipher import AES
from padding import pad, unpad
from utils import base64_to_bytes, bytes_to_base64
from Crypto.Util.Padding import PaddingError

"""
In ECB mode, each message is divided into blocks, and each block is encrypted separately.
The disadvantage of this mode is that it is deterministic, meaning that the same plaintext
block will always produce the same ciphertext block. This means that patterns in the plaintext
will be visible in the ciphertext.
"""

def ecb_encrypt(key: bytes, message: bytes) -> bytes:
  """
  Encrypts a message using the Electronic Codebook (ECB) mode of operation for a block cipher
  params:
    * key: the key to use for encryption - 128 bits (16 bytes) for AES
    * message: the message to encrypt - arbitrary-length bytes
  """
  padded = pad(message, AES.block_size)
  cipher = AES.new(key, AES.MODE_ECB)
  ciphertext = cipher.encrypt(padded)
  return ciphertext


def ecb_decrypt(key: bytes, ciphertext: bytes) -> bytes:
  """
  Decrypts a message using the Electronic Codebook (ECB) mode of operation for a block cipher
  """
  cipher = AES.new(key, AES.MODE_ECB)
  try:
    padded = cipher.decrypt(ciphertext)
    message = unpad(padded)
    return message
  except ValueError:
    raise ValueError("Invalid ciphertext length or padding error")
  except PaddingError:
    raise ValueError("Padding error")


def detect_ecb(ciphertext: bytes, block_size: int) -> bool:
  """
  Detects if a ciphertext was encrypted using ECB mode of operation for a block cipher
  """
  pass


def create_ebc_cookie(userdata: bytes) -> bytes:
  """
  Creates a cookie using ECB mode of operation for a block cipher
  """
  pass
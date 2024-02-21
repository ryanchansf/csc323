from Crypto.Cipher import AES
from padding import pad, unpad
from utils import base64_to_bytes, bytes_to_base64

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


def decrypt_ecb(key: bytes, input_file: str) -> str:
  """
  Decrypts a file encrypted using ECB mode of operation for a block cipher
  """
  with open(input_file, "r") as f:
    ciphertext = base64_to_bytes(f.read())
  message = ecb_decrypt(key, ciphertext)
  return message.decode("utf-8")
  

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


if __name__ == "__main__":
  # Test ECB mode
  key = "CALIFORNIA LOVE!".encode("utf-8")
  file = "Lab2.TaskII.A.txt"
  print(decrypt_ecb(key, file))
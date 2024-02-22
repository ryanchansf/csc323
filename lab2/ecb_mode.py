from Crypto.Cipher import AES
from padding import pad, unpad
from utils import base64_to_bytes, bytes_to_base64, hex_to_bytes, bytes_to_hex

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
  """
  Lab2.TaskII.B.txt contains 100 hex-encoded encryptions of the same bitmap image. 
  One of them has been encrypted using AES in ECB mode, while the other 99 have been 
  encrypted using a semantically secure mode. Write some code that automatically 
  detects ECB ciphertexts. Note that the first 54 bytes of the strings are the unencrypted 
  BMP header, so the actual ciphertext blocks start at byte 54. When you think you’ve 
  identified the ECB-encrypted image you can try viewing it (as an image) and see how it 
  compares to the others.
  """
  # split the ciphertext into blocks
  blocks = [ciphertext[i : i + block_size] for i in range(0, len(ciphertext), block_size)]
  # check if any blocks are repeated
  return len(blocks) != len(set(blocks))


def identify_ecb_encrypted_image(input_file: str, block_size: int) -> int:
  with open(input_file, "r") as file:
    lines = file.readlines()

  for i, line in enumerate(lines):
    ciphertext = hex_to_bytes(line.strip())
    if detect_ecb(ciphertext[54:], block_size):
      with open("image.bmp", "wb") as f:
        f.write(ciphertext)
      return i + 1
  return -1


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

  # Identify ECB mode
  file = "Lab2.TaskII.B.txt"
  block_size = AES.block_size
  print("ECB message found at line:", identify_ecb_encrypted_image(file, block_size))

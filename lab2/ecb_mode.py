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
  

def detect_ecb(ciphertext: bytes, block_size: int) -> bool:
  """
  Detects if a ciphertext was encrypted using ECB mode of operation for a block cipher
  """
  # split the ciphertext into blocks
  blocks = [ciphertext[i : i + block_size] for i in range(0, len(ciphertext), block_size)]
  # check if any blocks are repeated
  return len(blocks) != len(set(blocks))


def identify_ecb_encrypted_image() -> None:
  """
  Go through the lines of the file Lab2.TaskII.B.txt and identify the line that contains an image encrypted using ECB mode
  """
  block_size = AES.block_size
  with open("Lab2.TaskII.B.txt", "r") as file:
    lines = file.readlines()

  for i, line in enumerate(lines):
    ciphertext = hex_to_bytes(line.strip())
    if detect_ecb(ciphertext[54:], block_size):
      with open("image.bmp", "wb") as f:
        f.write(ciphertext)
      print("ECB message found at line:", i + 1)
      print("Image saved as image.bmp")


def test_ecb_decrypt() -> None:
  """
  Decrypt the message in Lab2.TaskII.A.txt using the key "CALIFORNIA LOVE!" and print the result
  """
  key = "CALIFORNIA LOVE!".encode("utf-8")
  with open("Lab2.TaskII.A.txt", "r") as file:
    ciphertext = base64_to_bytes(file.read())
    
  message = ecb_decrypt(key, ciphertext)
  print(message.decode("utf-8"))


if __name__ == "__main__":
  # Test ECB mode
  test_ecb_decrypt()

  # Identify ECB mode
  identify_ecb_encrypted_image()

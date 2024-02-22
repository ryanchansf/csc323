import base64
from Crypto.Cipher import AES
from padding import pad, unpad
from utils import base64_to_bytes, bytes_to_base64
import requests

def cbc_encrypt(key: bytes, iv: bytes, plaintext: bytes) -> bytes:
    """
    Encrypts a message using the Cipher Block Chaining (CBC) mode of operation for a block cipher
    """
    encrypted_message = b""
    previous_block = iv
    cipher = AES.new(key, AES.MODE_ECB)

    plaintext = pad(plaintext, AES.block_size)

    for i in range(0, len(plaintext), AES.block_size):
      block = plaintext[i:i+AES.block_size]  # pull out next block
      block = bytes([a ^ b for a, b in zip(block, previous_block)])  # XOR with previous block
      encrypted_block = cipher.encrypt(block)
      encrypted_message += encrypted_block
      previous_block = encrypted_block

    return encrypted_message

def cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
  """
  Decrypts a message using the Cipher Block Chaining (CBC) mode of operation for a block cipher
  """
  decrypted_message = b""
  previous_block = iv
  cipher = AES.new(key, AES.MODE_ECB)

  for i in range(AES.block_size, len(ciphertext), AES.block_size):
    block = ciphertext[i:i+AES.block_size]  # pull out next block
    decrypted_block = cipher.decrypt(block)
    decrypted_block = bytes([a ^ b for a, b in zip(decrypted_block, previous_block)])  # XOR with previous block
    decrypted_message += decrypted_block
    previous_block = block

  decrypted_message = unpad(decrypted_message)

  return decrypted_message

def test_cbc_decrypt():
  key="MIND ON MY MONEY"
  iv="MONEY ON MY MIND"
  with open("Lab2.TaskIII.A.txt", "rb") as file:
    ciphertext = file.read()

  ciphertext = base64.b64decode(ciphertext)  # Decode base64-encoded ciphertext
  decrypted_text = cbc_decrypt(key.encode(), iv.encode(), ciphertext)
  print(decrypted_text.decode())


if __name__ == "__main__":
  test_cbc_decrypt()
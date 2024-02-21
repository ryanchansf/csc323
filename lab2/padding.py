"""
Block ciphers take as input a fixed-length key of k-bits,
and a plaintext block of n-bits, and outputs a fixed-length n-bit ciphertext block.
This means that the message you want to encrypt must be multiple of the cipher's block size
If it's not, a message must be padded. The trick with padding is that it must be unambiguous 
which are the pad bytes and which are the message bytes. But what's more, it mmust return an
error if the padding is incorrect. There are a number of approaches. You're going to implement
one.
"""

def pad(message: bytes, block_size: int) -> bytes:
  """
  Implement a PKCS#7 padding scheme for a block cipher
  """
  padding = block_size - len(message) % block_size
  return message + bytes([padding] * padding)
  

def unpad(padded_message: bytes) -> bytes:
  """
  Implement the PKCS#7 unpadding scheme for a block cipher
  """
  padding = padded_message[-1]
  if padding == 0 or padding > len(padded_message):
    raise ValueError("Incorrect padding")
  for i in range(1, padding):
    if padded_message[-i-1] != padding:
      raise ValueError("Incorrect padding")
  return padded_message[:-padding]
  
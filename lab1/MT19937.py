#Mersenne Twister MT 19937
class MT19937:
	def __init__(self, seed: bytes):
		#TODO: Initialize MT state here
		self.w = 32 # word size
		self.n = 624 # degree of recurrence
		self.m = 397 # middle word, an offset used in the recurrence relation defining the series x, 1 ≤ m < n
		self.r = 31 # separation point of one word, or the number of bits of the lower bitmask, 0 ≤ r ≤ w - 1
		self.a = 0x9908B0DF # coefficients of the rational normal form twist matrix
		self.u = 11 # additional Mersenne Twister tempering bit shifts/masks
		self.d = 0xFFFFFFFF
		self.s = 7 # additional Mersenne Twister tempering bit shifts/masks
		self.b = 0x9D2C5680 # additional Mersenne Twister tempering bit shifts/masks
		self.t = 15 # additional Mersenne Twister tempering bit shifts/masks
		self.c = 0xEFC60000 # additional Mersenne Twister tempering bit shifts/masks
		self.l = 18 # additional Mersenne Twister tempering bit shifts/masks
		self.f = 1812433253 # constant, a prime number
		
        # Create a length n array to store the state of the generator
		self.MT = [0 for i in range(self.n)]
		self.index = self.n + 1
		self.lower_mask = (1 << self.r) - 1 # the binary number of r number of 1's
		self.upper_mask = ((1 << self.w) - 1) & (~self.lower_mask) # the 32-bit binary number of (w-r) number of 1's
		self.seed_mt(seed) # Initialize the generator from a seed
	

	def seed_mt(self, seed: bytes):
		"""
		Initialize the random generator from a seed
		"""
		self.index = self.n
		self.MT[0] = int.from_bytes(seed, byteorder='big')
		for i in range(1, self.n): # loop over each element
			self.MT[i] = (self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i) & ((1 << self.w) - 1)
			# TODO: check & 0xFFFFFFFF equivalence with & ((1 << self.w) - 1) for getting lowest w bits
		return
		

	def extract_number(self) -> int:
		"""
		Extract a tempered value based on MT[index]
		calling twist() every n numbers
		"""
		#TODO: Temper and Extract Here
		if self.index >= self.n:
			if self.index > self.n:
				print("Generator was never seeded")
				return
			self.twist()

		y = self.MT[self.index] # Extract a tempered value based on MT[index]
		y = y ^ ((y >> self.u) & self.d) # Tempering
		y = y ^ ((y << self.s) & self.b) # Tempering
		y = y ^ ((y << self.t) & self.c) # Tempering
		y = y ^ (y >> self.l) # Tempering

		self.index += 1
		return y & ((1 << self.w) - 1) # return lowest w bits of y


	def twist(self):
		"""
		Generate the next n values from the series x_i
		"""
		#TODO: Mix state here
		for i in range(self.n):
			x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
			xA = x >> 1
			if (x % 2) != 0:
				xA = xA ^ self.a
			self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
		self.index = 0 # reset index
		return


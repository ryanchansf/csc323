import time
import random
from MT19937 import MT19937
from utils import *

def oracle() -> str:
    """
    Generate a random number as a base64 encoded string using the MT19937 PRNG

    1. Waits between 5 and 60 seconds, chosen randomly. 
    2. Seeds MT19937 using the current UNIX timestamp.
    3. Waits another randomly chosen number of seconds between 5 and 60.
    4. Return the first 32 bit output as a base64 encoded value.
    """
    time.sleep(random.randint(5, 60)) # random wait time between 5 and 60 seconds
    seed = int(time.time()) # current UNIX timestamp
    print("Generated Seed: ", seed)
    mt = MT19937(seed.to_bytes(4, byteorder="big")) # seed the MT19937 PRNG
    time.sleep(random.randint(5, 60)) # wait another randomly chose time
    output = mt.extract_number()
    return bytes_to_base64(output.to_bytes(4, byteorder="big")) # return 32 bit output


def find_seed(output: str) -> int:
    """
    Break seed given a 32 bit output from the MT19937 PRNG through brute force
    """
    current_time = int(time.time())
    # test the last 120 seconds for seed
    for seed in range(current_time, current_time - 120, -1):
        mt = MT19937(seed.to_bytes(4, byteorder="big")) # seed the MT19937 PRNG
        if mt.extract_number() == int.from_bytes(base64_to_bytes(output), byteorder="big"): # check if output matches the PRNG output
            print("Found seed: ", seed)
            return seed
    return -1


def main():
    output = oracle()
    print("Output: ", output)
    seed = find_seed(output)
    print("Guess: ", seed)


if __name__ == "__main__":
    main()
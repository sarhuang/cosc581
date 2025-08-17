#Inspired by: https://asecuritysite.com/encryption/nprimes


import sys
import libnum
import random
from tqdm import tqdm

#Miller-Rabin primality test
def miller_rabin(n, rounds=5):  
    if n <= 3:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False

    #Write n-1 as 2^s * d
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    for i in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for j in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True



#Set bitsize (lookings for command line)
bitsize = 2048
if len(sys.argv) > 1:
    bitsize = int(sys.argv[1])
else:
    print("Usage: ./exe bitsize")
    sys.exit(1)

#Generate q, then p = 2q + 1 and check both are prime
attempt = 0
with tqdm(desc="Searching for safe prime (p = 2q + 1)", unit=" attempt") as pbar:
    while True:
        q = libnum.generate_prime(bitsize - 1)
        p = 2 * q + 1
        attempt += 1
        pbar.update(1)
        if miller_rabin(p):
            break

N = p * q


print("Prime (p = 2q + 1): ", p)
print("Prime (q): ", q)
print("N = p * q: ", N)

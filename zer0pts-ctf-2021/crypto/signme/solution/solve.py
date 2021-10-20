from math import gcd
from ptrlib import *

sock = Socket("localhost", 10298)

# fault attack
payload = b"A" * (1024 // 8 - 3)
sock.sendlineafter(": ", payload)

r = sock.recvregex("m = ([0-9a-f]+)")
m = int(r[0], 16)
r = sock.recvregex("pubkey = \(([0-9a-f]+), ([0-9a-f]+)\)")
N, e = int(r[0], 16), int(r[1], 16)
r = sock.recvregex("signature = ([0-9a-f]+)")
s = int(r[0], 16) # here we get a broken signature

# factorize N
q = gcd(m - pow(s, e, N), N)
assert N % q == 0
p = N // q
phi = (p-1) * (q-1)
d = inverse(e, phi)

# find signature
r = sock.recvregex("message: ([0-9a-f]+)")
m = int(r[0], 16)
s = pow(m, d, N)
sock.sendlineafter("Signature: ", hex(s)[2:])

sock.interactive()

import random
import base64
from Crypto.Cipher import AES
from ptrlib import *

decoder = """
CNOT 0,2; CNOT 0,1;
CNOT 3,5; CNOT 3,4;
CNOT 6,8; CNOT 6,7;
H 0; CNOT 1,0; Tdag 0; CNOT 2,0; T 0; CNOT 1,0; Tdag 0; CNOT 2,0; T 0; H 0; T 1; CNOT 2,1; Tdag 1; T 2; CNOT 2,1;
H 3; CNOT 4,3; Tdag 3; CNOT 5,3; T 3; CNOT 4,3; Tdag 3; CNOT 5,3; T 3; H 3; T 4; CNOT 5,4; Tdag 4; T 5; CNOT 5,4;
H 6; CNOT 7,6; Tdag 6; CNOT 8,6; T 6; CNOT 7,6; Tdag 6; CNOT 8,6; T 6; H 6; T 7; CNOT 8,7; Tdag 7; T 8; CNOT 8,7;
H 0; H 3; H 6;
CNOT 0,6; CNOT 0,3;
H 0; CNOT 3,0; Tdag 0; CNOT 6,0; T 0; CNOT 3,0; Tdag 0; CNOT 6,0; T 0; H 0; T 3; CNOT 6,3; Tdag 3; T 6; CNOT 6,3;
""".replace("\n", "")

N = 128
xi, xip = 0.98, 0.98
p = (xi * (1 + xi))**0.5 - xi
Np = int(N * (1 + 2*xi + 2*(xi*(1+xi))**0.5 + xip))

#sock = Process(["python", "server.py"], cwd='../challenge')
sock = Socket("localhost", 11099)

bb = 0
for i in range(Np):
    bb <<= 1
    if random.choices([1, 0], [p, 1-p])[0] == 1:
        sock.sendlineafter("Circuit: ", decoder + "H 0;")
        bb |= 1
    else:
        sock.sendlineafter("Circuit: ", decoder)

rb = int(sock.recvlineafter("state: "), 2)
sock.sendlineafter("bb = ", bin(bb))

# We don't use these values now but they are necessary in the real world
# because we need to know how much quantum error happened.
# They are used to ensure nobody sniffed the network.
ba = int(sock.recvlineafter("ba = "), 2)
xa = int(sock.recvlineafter("xa = "), 2)

xb = 0
for i in range(Np):
    if (ba >> i) & 1 == (bb >> i) & 1 == 1:
        xb = (xb << 1) | ((rb >> i) & 1)
print(f"[+] xa = {bin(xa)}")
print(f"[+] xb = {bin(xb)}")

l = []
for i in range(Np):
    if (ba >> i) & 1 == (bb >> i) & 1 == 0:
        l.append(i)
m = int(sock.recvlineafter("m = "), 2)
for i in range(Np):
    if (m >> i) & 1:
        l.remove(i)

k = 0
for i in sorted(l):
    k = (k << 1) | ((rb >> i) & 1)

data = base64.b64decode(sock.recvlineafter(": "))
iv = data[:16]
ct = data[16:]

key = int.to_bytes(k, N // 8, 'big')
cipher = AES.new(key, AES.MODE_CBC, iv)
print(cipher.decrypt(ct))

sock.interactive()

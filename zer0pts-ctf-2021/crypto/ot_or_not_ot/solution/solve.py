from ptrlib import Socket
from Crypto.Cipher import AES
import base64
import os

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "9999")

sock = Socket(HOST, int(PORT))

b = base64.b64decode(sock.recvlineafter("flag: "))
iv, cipher = b[:AES.block_size], b[AES.block_size:]

p = int(sock.recvlineafter("p = "))
keylen = int(sock.recvlineafter("() = "))

binflag = ""
for i in range((keylen + 1) // 2):
    print(i)
    t = int(sock.recvlineafter("t = "))

    a = 2
    b = p - a
    c = pow(t, -1, p)
    d = pow(a, -1, p)

    sock.sendlineafter("a = ", str(a))
    sock.sendlineafter("b = ", str(b))
    sock.sendlineafter("c = ", str(c))
    sock.sendlineafter("d = ", str(d))

    x = int(sock.recvlineafter("x = "))
    y = int(sock.recvlineafter("y = "))
    z = int(sock.recvlineafter("z = "))

    u = pow(z, -1, p)
    v = -u % p

    m0 = x ^ u

    if x == y or x == -y % p:
        # (m0 == m1 and r is even) or (m0 == m1 and r is odd)
        m1 = m0
    elif abs(x - y) == 1 or abs(x - (-y%p)) == 1:
        # (m0 != m1 and r is even) or (m0 != m1 and r is odd)
        m1 = m0 ^ 1
    else:
        raise ValueError("WOW")

    binflag += str(m0)
    binflag += str(m1)


key = int.to_bytes(int(binflag[::-1], 2), 32, 'big')
aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
flag = aes.decrypt(cipher)
print(flag)

sock.close()

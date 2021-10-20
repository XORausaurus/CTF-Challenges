from ptrlib import Socket
import random
import os

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "9999")

def legendre_symbol(a, p):
    ls = pow(a, (p - 1)//2, p)
    if ls == p - 1:
        return -1
    return ls

while True:
    sock = Socket(HOST, int(PORT))
    g, p = sock.recvregex("g: ([0-9]+), and p: ([0-9]+)")
    g, p = int(g), int(p)


    # check parameter
    try:
        assert legendre_symbol(1, p) == 1
        assert legendre_symbol(2, p) != 1
        assert legendre_symbol(3, p) != 1

        for _ in range(100):
            m = random.randint(1, 3)
            c = m * pow(g, random.randint(2, p-1), p) % p
            assert legendre_symbol(m, p) == legendre_symbol(c, p)
    except AssertionError:
        sock.close()
        continue
    break

while True:
    c1, c2 = eval(sock.recvlineafter("="))

    qr = legendre_symbol(c2, p)
    if qr == 1:
        sock.sendlineafter("(1-3): ", "3")
    else:
        sock.sendlineafter("(1-3): ", "2")

    sock.recvline()
    sock.recvline()
    sock.recvline()
    result = sock.recvline().decode()
    if "draw" in result:
        pass

    elif "ahaha" in result:
        print("[-] something wrong")
        exit()

    elif "win" in result:
        wins = int(sock.recvlineafter("wins: "))
        print("wins: {}".format(wins))
        if wins >= 100:
            break

print(sock.recvuntil("}").decode())

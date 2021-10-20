import random
from ptrlib import u32
from collections import namedtuple

LIST_ALU = [
    'ADD', 'SUB', 'MUL', 'DIV',
    'OR', 'AND', 'LSH', 'RSH',
    'NEG', 'MOD', 'XOR'
]
LIST_JMP = [
    'JA', 'JEQ', 'JGT', 'JGE', 'JSET'
]

def seccompify(program):
    output = ''

    for pos, instr in enumerate(program):
        flags = []
        arg = 0
        if instr.opecode == 'LOAD' or instr.opecode == 'LOADX':
            # 特殊代入演算
            if instr.opecode == 'LOAD':
                flags.append('BPF_LD')
            else:
                flags.append('BPF_LDX')
            # ビット幅
            if instr.size == 32:
                flags.append('BPF_W')
            elif instr.size == 16:
                flags.append('BPF_H')
            elif instr.size == 8:
                flags.append('BPF_B')
            if instr.operand == 'nr':
                # システムコール番号
                flags.append('BPF_ABS')
                arg = '(offsetof(struct seccomp_data, nr))'
            elif 'args' in str(instr.operand):
                # システムコール引数
                flags.append('BPF_ABS')
                arg = f'(offsetof(struct seccomp_data, {instr.operand}))'
            elif 'mem' in str(instr.operand):
                # メモリ
                flags.pop()
                flags.append('BPF_MEM')
                arg = int(instr.operand[
                    instr.operand.index('[')+1 : instr.operand.index(']')
                ])
            else:
                # 即値
                flags.append('BPF_IMM')
                arg = int(instr.operand)
            output += 'BPF_STMT({}, {}),\n'.format('|'.join(flags), arg)

        elif instr.opecode == 'STORE':
            # 特殊格納
            flags.append('BPF_ST')
            arg = int(instr.operand)
            output += 'BPF_STMT({}, {}),\n'.format('|'.join(flags), arg)

        elif instr.opecode in LIST_ALU:
            # 算術演算
            flags.append('BPF_ALU')
            flags.append('BPF_' + instr.opecode)
            if instr.operand == 'reg':
                # レジスタ
                flags.append('BPF_X')
            else:
                # 即値
                flags.append('BPF_K')
                arg = int(instr.operand)
            output += 'BPF_STMT({}, {}),\n'.format('|'.join(flags), arg)

        elif instr.opecode in LIST_JMP:
            flags.append('BPF_JMP')
            flags.append('BPF_' + instr.opecode)
            flags.append('BPF_K')
            # ラベルを探す
            if instr.jt == 0:
                jt = 0
            else:
                for p, i in enumerate(program):
                    if i.label == instr.jt:
                        jt = p - pos - 1
                        assert jt > 0
                        break
                else:
                    print(f"[-] label '{instr.jt}' not found")
                    exit(1)
            if instr.jf == 0:
                jf = 0
            else:
                for p, i in enumerate(program):
                    if i.label == instr.jf:
                        jf = p - pos - 1
                        assert jf > 0
                        break
                else:
                    print(f"[-] label '{instr.jf}' not found")
                    exit(1)
            if instr.opecode == 'JA':
                output += 'BPF_JUMP({}, {}, 0, 0),\n'.format(
                    '|'.join(flags), jt
                )
            else:
                output += 'BPF_JUMP({}, {}, {}, {}),\n'.format(
                    '|'.join(flags), instr.operand, jt, jf
                )

        elif instr.opecode == 'RET':
            flags.append('BPF_RET')
            flags.append('BPF_K')
            if instr.operand == 'allow':
                arg = 'SECCOMP_RET_ALLOW'
            elif instr.operand == 'kill':
                arg = 'SECCOMP_RET_KILL'
            else:
                arg = f'SECCOMP_RET_ERRNO | ({instr.operand}&SECCOMP_RET_DATA)'
            output += 'BPF_STMT({}, {}),\n'.format('|'.join(flags), arg)

        else:
            print(f"[-] Invalid opecode 'instr.opecode'")
            exit(1)

    return output

Ope = namedtuple('Instruction',
                 ('opecode', 'operand', 'jt', 'jf', 'size', 'label'))
Ope.__new__.__defaults__ = (None, None, 0, 0, 32, '')

flag = b'zer0pts{B3rk3l3y_P4ck3t_F1lt3r:Y3t_4n0th3r_4ss3mbly}\0\0\0\0'
ansList = []
for i in range(14):
    args = [
        u32(flag[i*4:i*4+4]),
        u32(flag[(i*4+4)%56:(i*4+8)%56]),
        u32(flag[(i*4+8)%56:(i*4+12)%56]),
        u32(flag[(i*4+12)%56:(i*4+16)%56]),
    ]
    x0 = args[0]
    x1 = x0 ^ args[1]
    x2 = x1 ^ args[2]
    x3 = x2 ^ args[3]

    y0 = (x0 + x1 + x2 + x3) % 0x100000000
    y1 = (x0 - x1 + x2 - x3) % 0x100000000
    y2 = (x0 + x1 - x2 - x3) % 0x100000000
    y3 = (x0 - x1 - x2 + x3) % 0x100000000

    ansList.append(
        ((y0 | y1) ^ (y2 & y3),
         (y1 | y2) ^ (y3 & y0),
         (y2 | y3) ^ (y0 & y1),
         (y3 | y0) ^ (y1 & y2))
    )

program = [
    # Check system call number
    Ope('LOAD', 'nr', size=32),
    Ope('JEQ', 777, jf='pass'),

    # ASCII check
    Ope('LOAD', 'args[0]'),
    Ope('AND', 0xff),
    Ope('JGE', 0x80, jt='ng'),
    Ope('LOAD', 'args[0]'),
    Ope('RSH', 8),
    Ope('AND', 0xff),
    Ope('JGE', 0x80, jt='ng'),
    Ope('LOAD', 'args[0]'),
    Ope('RSH', 16),
    Ope('AND', 0xff),
    Ope('JGE', 0x80, jt='ng'),
    Ope('LOAD', 'args[0]'),
    Ope('RSH', 24),
    Ope('AND', 0xff),
    Ope('JGE', 0x80, jt='ng'),

    # Store XORed values
    Ope('LOAD', 'args[0]'),
    Ope('STORE', 0), # mem[0] = args[0]
    Ope('LOAD', 'args[1]'),
    Ope('LOADX', 'mem[0]'),
    Ope('XOR', 'reg'),
    Ope('STORE', 1), # mem[1] = args[0] ^ args[1]
    Ope('LOAD', 'args[2]'),
    Ope('LOADX', 'mem[1]'),
    Ope('XOR', 'reg'),
    Ope('STORE', 2), # mem[2] = args[0] ^ args[1] ^ args[2]
    Ope('LOAD', 'args[3]'),
    Ope('LOADX', 'mem[2]'),
    Ope('XOR', 'reg'),
    Ope('STORE', 3), # mem[3] = args[0] ^ args[1] ^ args[2] ^ args[3]

    # Calculate values
    Ope('LOAD', 'mem[0]'),
    Ope('LOADX', 'mem[1]'),
    Ope('ADD', 'reg'),
    Ope('LOADX', 'mem[2]'),
    Ope('ADD', 'reg'),
    Ope('LOADX', 'mem[3]'),
    Ope('ADD', 'reg'),
    Ope('STORE', 4), # mem[4] = x0 + x1 + x2 + x3
    Ope('LOAD', 'mem[0]'),
    Ope('LOADX', 'mem[1]'),
    Ope('SUB', 'reg'),
    Ope('LOADX', 'mem[2]'),
    Ope('ADD', 'reg'),
    Ope('LOADX', 'mem[3]'),
    Ope('SUB', 'reg'),
    Ope('STORE', 5), # mem[5] = x0 - x1 + x2 - x3
    Ope('LOAD', 'mem[0]'),
    Ope('LOADX', 'mem[1]'),
    Ope('ADD', 'reg'),
    Ope('LOADX', 'mem[2]'),
    Ope('SUB', 'reg'),
    Ope('LOADX', 'mem[3]'),
    Ope('SUB', 'reg'),
    Ope('STORE', 6), # mem[6] = x0 + x1 - x2 - x3
    Ope('LOAD', 'mem[0]'),
    Ope('LOADX', 'mem[1]'),
    Ope('SUB', 'reg'),
    Ope('LOADX', 'mem[2]'),
    Ope('SUB', 'reg'),
    Ope('LOADX', 'mem[3]'),
    Ope('ADD', 'reg'),
    Ope('STORE', 7), # mem[7] = x0 - x1 - x2 + x3

    # Calculate more
    Ope('LOAD', 'mem[4]'),
    Ope('LOADX', 'mem[5]'),
    Ope('OR', 'reg'),
    Ope('STORE', 8),
    Ope('LOAD', 'mem[6]'),
    Ope('LOADX', 'mem[7]'),
    Ope('AND', 'reg'),
    Ope('LOADX', 'mem[8]'),
    Ope('XOR', 'reg'),
    Ope('STORE', 8), # mem[8] = (y0 | y1) ^ (y2 & y3)
    Ope('LOAD', 'mem[5]'),
    Ope('LOADX', 'mem[6]'),
    Ope('OR', 'reg'),
    Ope('STORE', 9),
    Ope('LOAD', 'mem[7]'),
    Ope('LOADX', 'mem[4]'),
    Ope('AND', 'reg'),
    Ope('LOADX', 'mem[9]'),
    Ope('XOR', 'reg'),
    Ope('STORE', 9), # mem[8] = (y1 | y2) ^ (y3 & y0)
    Ope('LOAD', 'mem[6]'),
    Ope('LOADX', 'mem[7]'),
    Ope('OR', 'reg'),
    Ope('STORE', 10),
    Ope('LOAD', 'mem[4]'),
    Ope('LOADX', 'mem[5]'),
    Ope('AND', 'reg'),
    Ope('LOADX', 'mem[10]'),
    Ope('XOR', 'reg'),
    Ope('STORE', 10), # mem[8] = (y2 | y3) ^ (y0 & y1)
    Ope('LOAD', 'mem[7]'),
    Ope('LOADX', 'mem[4]'),
    Ope('OR', 'reg'),
    Ope('STORE', 11),
    Ope('LOAD', 'mem[5]'),
    Ope('LOADX', 'mem[6]'),
    Ope('AND', 'reg'),
    Ope('LOADX', 'mem[11]'),
    Ope('XOR', 'reg'),
    Ope('STORE', 11), # mem[8] = (y3 | y0) ^ (y1 & y2)
]

# Check result
program += [
    Ope('LOAD', 'mem[8]'),
]
qqq = list(range(14))
random.shuffle(qqq)
for i in qqq:
    program.append(
        Ope('JEQ', ansList[i][0], jt=f'c2-{i}')
    )
random.shuffle(qqq)
for i in qqq:
    program += [
        Ope('LOAD', 'mem[9]', label=f'c2-{i}'),
        Ope('JEQ', ansList[i][1], jf='ng', jt=f'c3-{i}')
    ]
random.shuffle(qqq)
for i in qqq:
    program += [
        Ope('LOAD', 'mem[10]', label=f'c3-{i}'),
        Ope('JEQ', ansList[i][2], jf='ng', jt=f'c4-{i}')
    ]
random.shuffle(qqq)
for i in qqq:
    program += [
        Ope('LOAD', 'mem[11]', label=f'c4-{i}'),
        Ope('JEQ', ansList[i][3], jf='ng', jt='ok')
    ]

program += [
    Ope('RET', 'allow', label='pass'),
    Ope('RET', 0, label='ok'),
    Ope('RET', 1, label='ng')
]
#"""

filt = seccompify(program)
print(filt)
with open("template.c", "r") as f:
    code = f.read()
with open("main.c", "w") as f:
    f.write(code.replace("%%%%", filt))

import os
os.system("make")
os.system("seccomp-tools dump ../distfiles/chall")

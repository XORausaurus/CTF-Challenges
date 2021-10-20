from ptrlib import u32
from z3 import *

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

s = Solver()
flag = [BitVec(f"flag{i}", 32) for i in range(14)]

s.add(flag[0] & 0xff == ord('z'))
for i in range(14):
    for j in range(4):
        c = (flag[i] >> (j * 8)) & 0xff
        s.add(c < 0x80)

for i in range(0, 14):
    x0 = flag[i]
    x1 = flag[i] ^ flag[(i+1) % 14]
    x2 = flag[i] ^ flag[(i+1) % 14] ^ flag[(i+2) % 14]
    x3 = flag[i] ^ flag[(i+1) % 14] ^ flag[(i+2) % 14] ^ flag[(i+3) % 14]

    y0 = x0 + x1 + x2 + x3
    y1 = x0 - x1 + x2 - x3
    y2 = x0 + x1 - x2 - x3
    y3 = x0 - x1 - x2 + x3

    a = (y0 | y1) ^ (y2 & y3)
    b = (y1 | y2) ^ (y3 & y0)
    c = (y2 | y3) ^ (y0 & y1)
    d = (y3 | y0) ^ (y1 & y2)

    constraints = []
    for i in range(14):
        fill = []
        fill.append(a == ansList[i][0])
        fill.append(b == ansList[i][1])
        fill.append(c == ansList[i][2])
        fill.append(d == ansList[i][3])
        constraints.append(And(fill))

    s.add(Or(constraints))

while True:
    r = s.check()
    if r == sat:
        m = s.model()
        answer = [b'????' for i in range(14)]
        for d in m.decls():
            answer[int(d.name()[4:])] = int.to_bytes(m[d].as_long(), 4, 'little')
        print(b''.join(answer))
        s.add(Not(And([flag[int(d.name()[4:])] == m[d] for d in m.decls()])))
    else:
        print(r)
        exit()

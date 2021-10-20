from mugi import Mugi

as1 = []
as2 = []
encoded = []
with open("../distfiles/output.txt", 'r') as f:
    for line in f:
        if len(as1) < 3:
            as1.append(int(line, 16))
        elif len(as2) < 3:
            as2.append(int(line, 16))
        else:
            encoded.append(int(line, 16))

key = b'\xf3\x28\x11\x0b\xde\x7a\xc4\x95\x5d\xef\x30\x37\x4f\x7e\xc2\xbb'
iv  = int.to_bytes(as1[0] ^ as2[0], 8, 'little')
iv += int.to_bytes(as1[1] ^ as2[1], 8, 'little')
mugi = Mugi(key, iv)

flag = ''
gen = mugi.prng()
for data in encoded:
    flag += chr(data ^ next(gen))

print(flag)

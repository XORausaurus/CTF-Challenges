import sys
import os

def encrypt(buf):
    offset = 0
    while b'\xab\xad\xf0\x0d' in buf[offset:]:
        offset += buf[offset:].index(b'\xab\xad\xf0\x0d')
        if buf[offset-3] & 0xf0 != 0xf0:
            offset += 4
            continue

        offset += 4

        # Find BOF marker
        for i in range(0x10, 0x30):
            if buf[offset-i] & 0xf0 == 0xb0 and buf[offset-i-1] & 0xf0 == 0x40:
                key = int.from_bytes(buf[offset-i+1:offset-i+8+1], 'little')
                break
        else:
            continue

        begin = offset

        # Find EOF marker
        for i in range(begin, len(buf)-4):
            if buf[i:i+4] == b'\x0d\xf0\xad\xab':
                end = i
                break
        else:
            continue

        print(f"[+] key = {hex(key)}")
        A = key & 0xffffffff
        B = key >> 32
        X = end - begin
        for i in range(begin, end-3):
            X = (A * X + B) & 0xffffffff
            n = int.from_bytes(buf[i:i+4], 'little')
            blk = int.to_bytes(n ^ X, 4, 'little')
            buf = buf[:i] + blk + buf[i+len(blk):]

    return buf

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <executable>')
        exit(1)

    path = sys.argv[1]
    if not os.path.isfile(path):
        print(f'Not a file: {path}')
        exit(1)

    with open(path, 'rb') as f:
        buf = f.read()

    with open('obfuscated', 'wb') as f:
        f.write(encrypt(buf))

    

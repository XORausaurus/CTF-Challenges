import re
import os
import sys


flag_plaintext = b'zer0pts{OISC_1s_th3_futur3~0xbuyd0g3!0xb1tc01n$vCQW04nFV+Wz}'
flag_ciphertext = b'\x22\x46\xc2\x17\x2a\x95\xcf\x76\xbd\xee\xa3\xa2\x61\xda\x77\x62\x4a\x55\x2b\x46\x50\xe6\xa0\x80\xb0\x68\x1e\x9f\x4a\x9b\xc9\x8c\x0a\xad\xaf\x2a\xdb\x31\xf4\x7d\x3f\x39\x53\xaf\xd3\x37\xc8\x99\xb9\x5e\xef\x37\xbe\xff\x12\x81\x09\xac\xba\x0c'


def usage():
    prog = os.path.basename(sys.argv[0])
    print("usage: {0} encrypt slow\n"
          "       {0} encrypt fast\n"
          "       {0} decrypt slow\n"
          "       {0} decrypt fast\n"
          .format(prog),
          file=sys.stderr, end="")


# MMIX by Donald Knuth from [1]
m = 18446744073709551616
a = 6364136223846793005
c = 1442695040888963407


# just a random number
seed = 17644285861079098374


def random():
    global seed
    seed = (seed * a + c) % m
    return seed


def skip_slow(n):
    for i in range(n):
        random()


def skip_fast(n):
    global seed
    x = seed
    b = c

    # expropriated from [2], but s/self//g
    a1 = a - 1
    ma = a1 * m
    y = (pow(a, n, ma) - 1) // a1 * b
    z = pow(a, n, m) * x
    x = (y + z) % m

    seed = x


def main():
    try:
        _, method, speed = sys.argv
        assert method in ['encrypt', 'decrypt']
        assert speed in ['slow', 'fast']
        if speed == 'slow':
            skip = skip_slow
        else:
            skip = skip_fast
        if method == 'encrypt':
            flag = flag_plaintext
            direction = +1
        else:
            flag = flag_ciphertext
            direction = -1
    except Exception:
        usage()
        sys.exit(1)

    output = []
    n = 1
    print("i\tx\tz\tsecret")
    for i, x in enumerate(flag):
        skip(n)
        secret = random()
        z = (x + direction * secret) % 256
        print("%d\t%r\t'\\x%02x'\t%016x" % (i, chr(x), z, secret))
        output.append(z)
        n = n * 2

    print()
    print("# Python")
    print("flag = %r" % bytes(output))

    print()
    print("// HSQ")
    print('int flag = "' + re.sub(r'(..)', r'\x\1', bytes(output).hex()) + '";')


if __name__ == '__main__':
    main()


# Links:
#
# [1]: https://en.wikipedia.org/wiki/Linear_congruential_generator#Parameters_in_common_use
# [2]: https://www.nayuki.io/res/fast-skipping-in-a-linear-congruential-generator/lcgrandom.py

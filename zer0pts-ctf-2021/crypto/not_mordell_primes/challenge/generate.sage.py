

# This file was *autogenerated* from the file generate.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_3 = Integer(3); _sage_const_5 = Integer(5); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1); _sage_const_512 = Integer(512); _sage_const_0x10001 = Integer(0x10001)
def solvable(a, b, p, P, N):
    EC = EllipticCurve(GF(p), [a, b])
    P = EC(P)

    # find l
    PR = PolynomialRing(GF(p), names=('x2', 'y2', 'l',)); (x2, y2, l,) = PR._first_ngens(3)
    x1, y1 = P.xy()

    x3 = l**_sage_const_2  - (x1 + x2)
    y3 = l*(x1 - x3) - y1

    I = Ideal([x2*x3 - N, (x2**_sage_const_3  + a*x2 + b) - (y2**_sage_const_2 ), (x3**_sage_const_3  + a*x3 + b) - (y3**_sage_const_2 ), l*(x2 - x1) - (y2 - y1)])
    B = I.groebner_basis()
    PR = PolynomialRing(GF(p), names=('x',)); (x,) = PR._first_ngens(1)
    f = x**_sage_const_2  + int(B[_sage_const_5 ][l])*x + int(B[_sage_const_5 ].constant_coefficient())

    ls = [r[_sage_const_0 ]**r[_sage_const_1 ] for r in f.roots()]

    # find y2
    for l in ls:
        PR = PolynomialRing(GF(p), names=('x2', 'y2',)); (x2, y2,) = PR._first_ngens(2)
        x3 = l**_sage_const_2  - (x1 + x2)
        y3 = l*(x1 - x3) - y1

        I = Ideal([x2*x3 - N, (x2**_sage_const_3  + a*x2 + b) - (y2**_sage_const_2 ), (x3**_sage_const_3  + a*x3 + b) - (y3**_sage_const_2 ), l*(x2 - x1) - (y2 - y1)])

        B = I.groebner_basis()
        f = x**_sage_const_2  + int(B[_sage_const_0 ][y2])*x + int(B[_sage_const_0 ].constant_coefficient())
        ys = [r[_sage_const_0 ]**r[_sage_const_1 ] for r in f.roots()]

        for y2 in ys:
            x2 = -B[_sage_const_1 ](y2=y2).constant_coefficient()
            if N % int(x2) == _sage_const_0 :
                return True
        return False


while True:
    p = random_prime(_sage_const_1  << _sage_const_512 )

    x1 = random_prime(p-_sage_const_1 )
    x2 = random_prime(p-_sage_const_1 )

    y1 = randint(_sage_const_0 , p-_sage_const_1 )
    y2 = randint(_sage_const_0 , p-_sage_const_1 )

    a = ((y1**_sage_const_2  - y2**_sage_const_2 ) - (x1**_sage_const_3  - x2**_sage_const_3 )) * inverse_mod(x1 - x2, p) % p
    b = (y1**_sage_const_2  - x1**_sage_const_3  - a*x1) % p

    EC = EllipticCurve(GF(p), [a, b])

    # check the points on curve
    Q = EC((x1, y1))
    R = EC((x2, y2))

    P = R - Q
    N = x1 * x2

    if solvable(a, b, p, P, N):
        break

with open("flag.txt", "rb") as f:
    m = int.from_bytes(f.read().strip(), "big")
e = _sage_const_0x10001 
c = pow(m, e, N)

with open("output.txt", "w") as f:
    print("N = {}".format(N), file=f)
    print("c = {}".format(c), file=f)

print("p = {}".format(p))
print("a = {}".format(a))
print("b = {}".format(b))
print("P = E{}".format(P.xy()))
print("Q = E{}".format(Q.xy()))
print("R = E{}".format(R.xy()))
print("N = {}".format(N))
print("c = {}".format(c))


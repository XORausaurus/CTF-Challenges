def solvable(a, b, p, P, N):
    EC = EllipticCurve(GF(p), [a, b])
    P = EC(P)

    # find l
    PR.<x2, y2, l> = PolynomialRing(GF(p))
    x1, y1 = P.xy()

    x3 = l^2 - (x1 + x2)
    y3 = l*(x1 - x3) - y1

    I = Ideal([x2*x3 - N, (x2^3 + a*x2 + b) - (y2^2), (x3^3 + a*x3 + b) - (y3^2), l*(x2 - x1) - (y2 - y1)])
    B = I.groebner_basis()
    PR.<x> = PolynomialRing(GF(p))
    f = x^2 + int(B[5][l])*x + int(B[5].constant_coefficient())

    ls = [r[0]^r[1] for r in f.roots()]

    # find y2
    for l in ls:
        PR.<x2, y2> = PolynomialRing(GF(p))
        x3 = l^2 - (x1 + x2)
        y3 = l*(x1 - x3) - y1

        I = Ideal([x2*x3 - N, (x2^3 + a*x2 + b) - (y2^2), (x3^3 + a*x3 + b) - (y3^2), l*(x2 - x1) - (y2 - y1)])

        B = I.groebner_basis()
        f = x^2 + int(B[0][y2])*x + int(B[0].constant_coefficient())
        ys = [r[0]^r[1] for r in f.roots()]

        for y2 in ys:
            x2 = -B[1](y2=y2).constant_coefficient()
            if N % int(x2) == 0:
                return True
        return False


while True:
    p = random_prime(1 << 512)

    x1 = random_prime(p-1)
    x2 = random_prime(p-1)

    y1 = randint(0, p-1)
    y2 = randint(0, p-1)

    a = ((y1^2 - y2^2) - (x1^3 - x2^3)) * inverse_mod(x1 - x2, p) % p
    b = (y1^2 - x1^3 - a*x1) % p

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
e = 0x10001
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


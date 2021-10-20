p = 13046889097521646369087469608188552207167764240347195472002158820809408567610092324592843361428437763328630003678802379234688335664907752858268976392979073
a = 10043619664651911066883029686766120169131919507076163314397915307085965058341170072938120477911396027902856306859830431800181085603701181775623189478719241
b = 12964455266041997431902182249246681423017590093048617091076729201020090112909200442573801636087298080179764338147888667898243288442212586190171993932442177

EC = EllipticCurve(GF(p),[a,b])

P = EC(11283606203023552880751516189906896934892241360923251780689387054183187410315259518723242477593131979010442607035913952477781391707487688691661703618439980, 12748862750577419812619234165922125135009793011470953429653398381275403229335519006908182956425430354120606424111151410237675942385465833703061487938776991)

import ast
with open("output.txt") as f:
    N = ast.literal_eval(f.readline().strip().split(" = ")[1])
    c = ast.literal_eval(f.readline().strip().split(" = ")[1])

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
    print("l = {}".format(l))
    PR.<x2, y2> = PolynomialRing(GF(p))
    x3 = l^2 - (x1 + x2)
    y3 = l*(x1 - x3) - y1

    I = Ideal([x2*x3 - N, (x2^3 + a*x2 + b) - (y2^2), (x3^3 + a*x3 + b) - (y3^2), l*(x2 - x1) - (y2 - y1)])

    B = I.groebner_basis()
    f = x^2 + int(B[0][y2])*x + int(B[0].constant_coefficient())
    ys = [r[0]^r[1] for r in f.roots()]

    for y2 in ys:
        print("y2 = {}".format(y2))
        x2 = -B[1](y2=y2).constant_coefficient()
        if N % int(x2) != 0:
            continue

        p = N // int(x2)
        q = N // p
        d = inverse_mod(0x10001, (p-1)*(q-1))
        m = pow(c, d, N)

        print(bytes.fromhex(hex(m)[2:]))

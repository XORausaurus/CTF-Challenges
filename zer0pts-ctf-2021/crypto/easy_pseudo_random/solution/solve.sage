from Crypto.Util.number import *
from small_roots import small_roots

nbits = 256
with open("output.txt") as f:
	while True:
		buf = f.readline()
		if not buf:
			break
		exec(buf)

Fp = Zmod(p)
P.<v> = PolynomialRing(Fp)
F = v^2 + b
Pf.<x, y> = PolynomialRing(Fp)

d = 2
k = ceil(nbits * (d / (d + 1)))
delta = float(1 / (d + 1))

bounds = (floor(p^delta), floor(p^delta))
f = (y + w1 * pow(2, nbits - k)) - ((x + w0 * pow(2, nbits - k))^2 + b)

res = small_roots(f, bounds)
print(res[0])

x0 = res[0][0]
x1 = res[0][1]
v0 = x0 + w0 * pow(2, nbits - k)
v1 = x1 + w1 * pow(2, nbits - k)
print(v0, v1)

v = v1
for i in range(5):
    v = F(v)
    m ^^= int(v)
print(long_to_bytes(m))

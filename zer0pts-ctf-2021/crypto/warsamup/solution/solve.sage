def pgcd(a, b):
  while b:
    a, b = b, a % b
  return a.monic()

def unpad(m: int):
  m = int(m).to_bytes((m.bit_length() + 7) // 8, "big")
  return m.split(b"\x00", 2)[-1]

exec(open("output.txt").read())

PR.<x> = PolynomialRing(Zmod(n))

c2_ = c2 * pow(2,e,n)%n
f1 = (x)^e - c1
f2 = (x - 1)^e - c2_

m = -pgcd(f1, f2)[0]
print(unpad(int(m)))

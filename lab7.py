from Crypto.Util.number import getPrime
import random as rnd
from lab5 import sha256
import math
from numpy import inf, isinf
from lab4 import div_by_mod, mul_by_mod

class Point(object):
  def __init__(self, elliptic_curve, x=None, y=None, is_zero=False):
    self.x = x
    self.y = y
    self.a = elliptic_curve.a
    self.b = elliptic_curve.b
    self.p = elliptic_curve.p
    self.elliptic_curve = elliptic_curve
    self.is_zero = is_zero

  def __eq__(self, other):
    return self.x == other.x and self.y == other.y and self.elliptic_curve == other.elliptic_curve

  def is_inverted(self, other):
    x1, y1 = self.x, self.y
    x2, y2 = other.x, other.y
    return y1%self.p == -y2%self.p and x1 == x2

  def __add__(self, other):
    x1, y1 = self.x, self.y
    x2, y2 = other.x, other.y
    if self.is_inverted(other):
      return Point(self.elliptic_curve, is_zero=True)
    if self.is_zero:
      return other
    if other.is_zero:
      return self
    dy, dx = (y2 - y1) % self.p, (x2 - x1) % self.p
    lambd = div_by_mod(dy, dx, self.p) if self != other else div_by_mod(3*(x1*x1) + self.a, 2*y1, self.p)
    x3 = ((lambd**2) - x1 - x2) % self.p
    y3 = (lambd*(x1 - x3) - y1) % self.p
    return Point(self.elliptic_curve, x3, y3)

  def __sub__(self, other):
    new = Point(self.elliptic_curve, other[0], -other[1])
    return self + new

  def double(self, P):
    return P + P

  def mul(self, P, n):
    if n == 1:
      return P
    if n % 2 == 0:
      return self.double(self.mul(P, n / 2))
    else:
      return self.mul(P, n - 1) + P

  def __mul__(self, n):
    return self.mul(self, n)

  def __rmul__(self, n):
    return self*n

class EllipticCurve(object):
  def __init__(self, a, b, p, x, y, n, h):
    self.a = a
    self.b = b
    self.p = p
    self.G = Point(self, x, y)
    self.n = n
    self.h = h

class ECDSA(object):
  def __init__(self, elliptic_curve):
    self.ec = elliptic_curve
    self.d = rnd.getrandbits(256)
    self.Q = self.d*self.ec.G
  
  def validate(self, M, r, s):
    if r <= 0 or r >= self.ec.n:
      return False
    if s <= 0 or s >= self.ec.n:
      return False
    alpha = sha256(M)
    e = alpha % self.ec.n
    e = 1 if e == 0 else e
    v = div_by_mod(1, e, self.ec.n)
    z1 = mul_by_mod(s, v, self.ec.n)
    z2 = mul_by_mod(-r, v, self.ec.n)
    C = z1*self.ec.G + z2*self.Q
    R = C.x % self.ec.n
    return R == r

  def generate(self, M):
    alpha = sha256(M)
    e = alpha % self.ec.n
    e = 1 if e == 0 else e
    while True:
      k = rnd.randrange(1, self.ec.n)
      C = k*  self.ec.G
      r = C.x % self.ec.n
      if r == 0:
        continue
      s = (r*self.d + k*e)% (self.ec.n)
      if s == 0:
        continue
      return r, s

if __name__ == '__main__':
  elliptic_curve = EllipticCurve(-3,
   0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
   2**256 - 2**224 + 2**192 + 2**96 - 1,
   0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
   0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5,
   0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
   1
  )
  ecdsa = ECDSA(elliptic_curve)
  r, s = ecdsa.generate(111)
  print ecdsa.validate(111, r, s)
from Crypto.Util.number import getStrongPrime
from primes_generator import generate
import random as rnd
from lab4 import div_by_mod, mul_by_mod
from other_primes_generator import PrimeGenerator
from lab5 import sha256

class DSAResult(object):
  def __init__(self, r, s):
    self.r, self.s = r, s

  def is_valid(self, m, p, q, g, y):
    if self.r <= 0 or self.r >= q:
      return False
    if self.s <= 0 or self.s >= q:
      return False
    w = div_by_mod(1, self.s, q)
    u1 = mul_by_mod(sha256(m), w, q)
    u2 = mul_by_mod(self.r, w, q)
    v = mul_by_mod(pow(g, u1, p), pow(y, u2, p), p) % q
    return v == self.r

class DSA(object):
  def __init__(self, l, n, seed_len):
    self.l = l
    self.n = n
    self.seed_len = seed_len 

  def generate(self, m):
    l, n, seed_len = self.l, self.n, self.seed_len
    p, q = PrimeGenerator(10).generate(2048, 224, 256)
    g = pow(2, (p - 1)/q, p)
    x = rnd.randrange(1, q)
    y = pow(g, x, p)
    k = rnd.randrange(1, q)
    r = pow(g, k, p) % q
    s = mul_by_mod(div_by_mod(1, k, q), sha256(m) + x*r, q)
    return DSAResult(r, s), p, q, g, y

if __name__ == '__main__':
  obj, p, q, g, y =  DSA(2048, 224, 256).generate(11111)
  print obj.is_valid(11111, p, q, g, y)






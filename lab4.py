from Crypto.Util.number import getStrongPrime
from Crypto.Random import random
from math import log

def egcd(a, b):
  if (a == 0):
      x, y = 0, 1 
      return b, x, y
  g, x, y = egcd(b % a, a)
  x, y = y - (b / a) * x, x
  return g, x, y

def it_egcd(a, b):
  states = []
  while a != 0:
    states.append((a, b))
    a,b = b%a, a
  g, x, y = b, 0, 1
  for a,b in reversed(states):
    x,y = y-(b/a)*x, x
  return g, x, y

def mul_by_mod(a, b, mod):
  return (a % mod * b % mod + mod) % mod

def div_by_mod(a, b, mod):
  g, x, y = it_egcd(b, mod)
  if (g == 1):
      x = (x % mod + mod) % mod
  return mul_by_mod(a, x, mod)

def generate_keys(size):
  a = getStrongPrime(size)
  b = getStrongPrime(size)
  n = a*b
  fi = (a - 1)*(b - 1)

  while(True):
    e = 2**(2**random.choice(range(5, int(log(size, 2) - 2)))) + 1
    if egcd(fi, e)[0] == 1:
      break

  d = div_by_mod(1, e, fi)
  return (e, n), (d, n)

def encrypt(public_key, open_text):
  e, n = public_key
  return pow(open_text, e, n)

def decrypt(private_key, cipher):
  d, n = private_key
  return pow(cipher, d, n)

if __name__ == '__main__':
  public_key, private_key = generate_keys(2048) 
  c = encrypt(public_key, 11111)
  m = decrypt(private_key, c)
  print c
  print m
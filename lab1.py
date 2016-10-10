from numpy import array, vstack, hstack, append

def caesar(string, key, alphabet):
  return ''.join([chr((ord(c) - ord('a') + key) % alphabet + ord('a')) for c in string])

def encode_skitala(string, n):
  length = len(string)
  a = array([list(string[i*n:(i+1)*n]) for i in xrange(length / n)])
  if length / n * n != length:
    a = vstack([a, [string[length / n * n + i] if length / n * n + i < length else '*' for i in xrange(n)]])
  return ''.join([''.join(a[:, i]) for i in xrange(n)])

def decode_skitala(string, n):
  m = len(string) / n
  a = [[string[j]] for j in xrange(m)]
  for i in xrange(1, n):
    a = append(a, [[string[i*m +j]] for j in xrange(m)], axis=1)
  return ''.join([''.join(a[i]) for i in xrange(m)]).rstrip('*')

def encode_scrambler(inp, i, j):
  res = ''
  for k, bit in enumerate(inp):
    bit = int(bit)
    if k - i >= 0:
      bit ^= int(res[k - i])
    if k - j >= 0:
      bit ^= int(res[k - j])
    res += str(bit)
  return res

def decode_scrambler(inp, i, j):
  res = ''
  for k, bit in enumerate(inp):
    bit = int(bit)
    if k - i >= 0:
      bit ^= int(inp[k - i])
    if k - j >= 0:
      bit ^= int(inp[k - j])
    res += str(bit)
  return res

if __name__ == '__main__':
  print caesar('abz', 27, 26)

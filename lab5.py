from Crypto.Hash import SHA256

table_h = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]

table_k = [
  0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5,
  0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174,
  0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA,
  0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967,
  0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85,
  0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070,
  0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3,
  0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2
]

def concat(a, b, length):
  return (a << length)^b

def concat_arr(arr, length):
  return reduce(lambda res, x: concat(res, x, length), arr)

def bits_count(nmb):
  return (len(hex(nmb).replace('L', '')) - 2)*4

def get_k(L):
  for k in xrange(512):
    if (k + L + 1) % 512 == 448:
      return k

def big_endian(nmb, n):
  res = []
  for i in xrange(n):
    res.append(str(nmb % 2))
    nmb /= 2
  return int(''.join(list(reversed(res))), 2)

def processed(message, L):
  m = concat(message, 1, 1)
  k = get_k(L)
  m = concat(m, 0, k)
  return concat(m, big_endian(L, 64), 64)

def get_bit(nmb, n):
  return (nmb & ( 1 << n )) >> n

def permutation(nmb, table):
  return reduce(lambda res, x: concat(res, get_bit(nmb, x), 1), table, 0)

def get_part_of_number(nmb, i, size):
  return permutation(nmb, reversed(list(range(i, i+size))))

def rotr(nmb, n):
  return ((nmb >> n) | ((nmb << (32 - n)) & ((1 << 32) - 1)))

def bitwise_not(nmb):
  return nmb ^ (2**32 - 1)

def s0(x):
  return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)

def s1(x):
  return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)

def get_parts(m):
  return reversed([get_part_of_number(m, i*512, 512) for i in xrange(bits_count(m) / 512)])

def get_w(part):
  w = list(reversed([get_part_of_number(part, i*32, 32) for i in xrange(16)]))
  for i in xrange(16, 64):
    w.append(add([w[i - 16], s0(w[i - 15]), w[i - 7], s1(w[i - 2])]))
  return w

def add(arr):
  return sum(arr) % (1<<32)

def sha256(message):
  length = len(str(message))*8
  import binascii
  message = int(binascii.hexlify(str(message)), 16)
  m = processed(message, length)
  H = table_h
  for part in get_parts(m):
    w = get_w(part)
    a, b, c, d, e, f, g, h = H
    for i in xrange(64):
      s0 = rotr(a, 2)^rotr(a, 13)^rotr(a, 22)
      Ma = (a&b)^(a&c)^(b&c)
      t2 = add([Ma,s0])
      s1 = rotr(e, 6)^rotr(e, 11)^rotr(e, 25)
      Ch = (e&f)^(bitwise_not(e)&g)
      t1 = add([h, s1, Ch, table_k[i], w[i]])
      h, g, f, e, d, c, b, a = g, f, e, add([d,t1]), c, b, a, add([t1,t2])
    H = map(add, zip(H, [a,b,c,d,e,f,g,h]))
  return concat_arr(H, 32)

def get_hash(seed):
  f = SHA256.new()
  f.update(str(seed))
  return int(f.hexdigest(), base=16)

if __name__ == '__main__':
  print hex(sha256(12341234123412341234123423412341234234123423412341234))
  print hex(get_hash(12341234123412341234123423412341234234123423412341234))

      
